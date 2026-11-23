{: .no_toc}
# Password Storage

> Design how a service stores usernames and passwords, so that stealing the database does not give an attacker the passwords.

- TOC
{:toc}

### 1. The goal

Users sign in with a password. We must be able to check a password, but we should never be able to read one. If the database leaks, the attacker should get nothing they can use quickly.

**Out of scope here:** sessions, OAuth and MFA. Section 9 gives a short note on bearer tokens, which is what a successful sign-in usually hands back.

### 2. The core decision: hash, do not encrypt

* **Encryption is reversible.** Whoever has the key gets every password back, and the key is usually not far from the data.
* **A hash is one way.** To check a login we hash what was typed and compare. The real password is never stored, so it cannot leak, and nobody at the company can read it.

### 3. What we store

One row per user, with the whole recipe in a single string:

```
users(id, username, password_hash, created_at)

password_hash = algorithm | cost settings | salt | hash
```

* **Algorithm:** a slow password hash. First choice **argon2id**, otherwise scrypt or bcrypt. Never plain SHA-256 or MD5, which are built to be fast.
* **Salt:** a random value, new for every user and every password change. It is not secret and is stored in the row. It makes identical passwords produce different hashes, so one precomputed table cannot crack everyone and "same hash, same password" tells an attacker nothing.
* **Cost settings:** how much time and memory each hash takes. Tune them so one check takes roughly 100 to 250 ms on our own servers: invisible to a user, ruinous to someone trying billions of guesses. The settings are stored with the hash so we can raise them later.
* **Hash:** the output.

### 4. Signing in

1. Look up the user and read the stored string.
2. Hash the typed password with *that row's* salt and settings.
3. Compare the two in constant time, so timing does not leak how much matched.
4. If the user does not exist, still do a dummy hash, so a fast "no such user" does not reveal who has an account.
5. Always answer "invalid username or password", never which part was wrong.

### 5. Upgrading hashes when the settings change

Computers get faster, so the cost has to go up over time, and the algorithm may change entirely. We cannot re-hash everyone at once, because we do not have their passwords. The answer is to upgrade **at login**.

**Two places hold settings, and they do different jobs:**

* **The user's row** holds the recipe that made *that* hash (algorithm and cost settings, inside the stored string). It is the version of that hash, so we always know how to verify it.
* **A separate table holds the current policy**, the recipe we want for new hashes:

```
password_policy(id, algorithm, cost_settings, pepper_version, created_at, is_current)
```

Only one row is current. Keeping it in a table (instead of in code) means every server reads the same value, we can change it without a deploy, and the old rows are a history of what we used and when.

**How we notice a change:**

1. A user signs in with the right password.
2. We read the recipe from the front of their stored string.
3. We compare it with the current row of `password_policy`.
4. If they match, we do nothing.
5. If they differ, we already hold the real password for this one moment, so we hash it again with the current policy and save the new string. Everyone who signs in moves to the new settings without a reset, and nobody notices.

Save with a check on the old value (update only if the hash is still the one we read), so two simultaneous logins cannot overwrite each other.

**Users who never come back** keep their old hashes. Options:

* **Wrap:** hash the old stored hash with the new algorithm, and record that it is layered. This upgrades everyone immediately, with no login. It is the standard way to get off a weak algorithm such as MD5.
* **Expire:** after a long period of inactivity, require a password reset.
* **Accept:** leave them, if the old settings are still reasonable.

### 6. Pepper (optional extra layer)

A pepper is a secret mixed into every hash. It is the **same for all users** and it is **kept outside the database**, in a key vault or hardware module, so a database leak does not include it.

* With a pepper, a stolen database is not even crackable until the attacker also breaks into the vault.
* **Costs:** losing it locks everyone out, and rotating it needs a version number in the stored string plus keeping old peppers until users have been re-hashed.
* It adds a layer. It does not replace a good slow hash with a salt.

### 7. What else the design needs

* **Rate limiting and lockouts** on sign-in, per account and per address. Slow hashing does not stop guessing through the login form.
* **Password rules** that favour length over symbols, and a check against lists of breached passwords.
* **MFA**, because passwords get reused and leaked elsewhere.
* **Password reset:** a single-use, short-lived random token, stored hashed. Never email the password.
* **Logging:** never record passwords, even failed ones.
* **Slow hashing is also a cost to us:** each sign-in uses CPU and memory, and an attacker can try to exhaust it. Rate limits protect that too.

### 8. Where encryption does belong

* **Secrets we must read back**, such as a third-party token we use on a user's behalf: encrypt with a modern authenticated cipher, with keys held in a key management service, not in the database.
* **API keys we issue** are different: like passwords, we only need to recognise them, so store a hash, show the key once, and allow rotation.

### 9. After sign-in: bearer tokens

Once the password is checked, the client usually gets a **bearer token** and sends it as `Authorization: Bearer <token>`. Whoever holds the token gets in, so it is treated like a password. The signed kind is the JWT, and the key points are:

* **Anyone can decode it.** The contents (user, expiry, scopes) are only Base64 text, not encrypted, so put nothing secret inside.
* **Only the holder of the private key can create one.** The issuer signs the contents with its private key, and everyone else verifies with the public key.
* **Why someone without the private key cannot create one:**
  * The signature is calculated from the exact contents plus the private key. Change one character, such as `user: 42` to `user: 1`, and the old signature no longer matches, so the token is rejected.
  * A new valid signature can only be produced with the private key.
  * The public key can verify a signature but cannot make one, and working out the private key from the public key is computationally infeasible.
* **Forging is impossible, but copying is not:** a stolen valid token works until it expires. So keep JWTs short-lived (minutes), send them only over TLS, and use a refresh token for longer sessions.
* **A JWT cannot be revoked before it expires.** Long-lived credentials, such as API keys, are better as random opaque tokens: stored as a hash, shown once, and revocable instantly.

### 10. Alternatives and trade-offs

* **Do not store passwords at all.** Sign-in with a provider (OAuth), passkeys, or magic links. Less to defend, but it depends on someone else. Passkeys are the strongest option where users can use them.
* **Higher cost or lower cost.** More cost slows attackers and us. Pick the highest cost that keeps login fast, and revisit it yearly.
* **Pepper or no pepper.** Extra safety against a database-only leak, against extra operational risk.
* **Upgrade at login, wrap, or force reset.** Login upgrades are free but incomplete. Wrapping covers everyone but is more complex. Resets are blunt.
* **Own the code or buy it.** Use a maintained library, or an identity provider. Do not write your own hashing.

### 11. Follow-ups to expect

**What if the database is stolen?** Attackers have slow salted hashes. Cracking is expensive per guess and per user, and the pepper, if used, is not in the database. Strong passwords hold. Weak ones eventually fall, which is why MFA matters.

**Why not SHA-256 with a salt?** It is too fast. Attackers can try billions of guesses a second. Password hashes are deliberately slow and use memory.

**How do you move from an old algorithm?** Upgrade at login, wrap the old hashes for the users who do not return, and track the algorithm in each row.

**How do you pick the cost?** Measure on production hardware, target a few hundred milliseconds, and raise it as hardware improves.

**What about password resets?** Short-lived, single-use tokens, stored hashed, sent to a verified channel.

**What if the pepper leaks?** Rotate: add a new version, keep the old one for verification, and re-hash users as they sign in.

Sources:

* [OWASP Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
* [NIST SP 800-63B: Digital Identity Guidelines](https://pages.nist.gov/800-63-3/sp800-63b.html)
