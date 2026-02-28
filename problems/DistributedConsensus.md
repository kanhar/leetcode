{: .no_toc}
# Distributed Consensus

- TOC
{:toc}
  
### [Number of nodes in a distributed network](https://leetcode.com/discuss/post/438213/print-the-number-of-nodes-in-a-distribut-3jxh/)

Develop a distributed consensus algorithm for an anonymous linear network of up to 10^6 nodes where each node lacks global positioning. 
Nodes must use local-only communication (Left/Right) to aggregate the total network count N and redistribute it so every node prints the value exactly once.

<details><summary markdown="span">Execute!</summary>

```python

class DefaultNode(AbstractNode):
    def __init__(self):
        self.has_printed = False

    def run(self):
        """
        The entry point executed on every node in the network.
        """
        # Scenario 1: Only one node in the network
        if not self.hasLeft() and not self.hasRight():
            print(1)
            self.has_printed = True
            return

        # Scenario 2: I am the Left Boundary (U). 
        # I start the accumulation wave.
        if not self.hasLeft():
            self.sendToRight(1)

    def receiveFromLeft(self, val: int):
        # Triggered when a node to my left calls sendToRight(). This is the 'Accumulation Phase'.        
        current_count = val + 1

        if not self.hasRight():
            # I am the Right Boundary (Z).  I now know the total count!
            print(current_count)
            self.has_printed = True            
            self.sendToLeft(current_count)
        else:
            # I am a middle node. Pass the incremented count right.
            self.sendToRight(current_count)

    def receiveFromRight(self, total_count: int):        
        # Triggered when a node to my right calls sendToLeft(). This is the 'Broadcast Phase'.                
        if not self.has_printed:
            print(total_count)
            self.has_printed = True

            # Continue passing the total count to the left
            if self.hasLeft():
                self.sendToLeft(total_count)
```

</details>
<BR>

### Leader Election

In a ring topology of nodes with unique IDs, the LCR algorithm achieves leader election by having each node propagate only the largest ID it encounters clockwise. 
When a node receives its own ID back, it identifies as the maximum value in the network and declares itself the leader.

<details><summary markdown="span">Execute!</summary>

```python
class LCRNode(AbstractNode):
    def __init__(self, node_id: int):
        self.node_id = node_id
        self.is_leader = False
        self.participant = False

    def run(self):
        """
        Entry point: Every node starts the election by sending its ID to the right.
        """
        # In a ring, every node has a right neighbor.
        self.sendToRight(self.node_id)
        self.participant = True

    def receiveFromLeft(self, received_id: int):
        """
        Triggered when the neighbor to the left passes an ID.
        """
        if received_id > self.node_id:
            # The incoming ID is a better candidate; forward it.
            self.sendToRight(received_id)
            self.participant = True
            
        elif received_id == self.node_id:
            # My own ID made it around the ring! I am the leader.
            self.is_leader = True
            print(f"Node {self.node_id}: I am the leader.")
            
            # Optional: Start a 'Termination' wave to inform others
            self.sendToRight(("LEADER_ANNOUNCEMENT", self.node_id))

        else:
            # received_id < self.node_id
            # Discard the message. I am a better candidate than the sender.
            pass

    def receiveFromRight(self, val):
        """
        Note: LCR is typically unidirectional. 
        In a standard LCR ring, this would remain unused unless 
        implementing a bidirectional variant.
        """
        pass
```

</details>
<BR>

### Distributed Max in Tree nodes

In a tree-structured network where each node possesses a local temperature reading, the goal is to identify and distribute the global maximum value across all nodes. 
Because nodes are only connected via parent-child relationships, the challenge lies in coordinating the flow of data across branches to ensure the root accurately captures and shares the overall peak value.

<details><summary markdown="span">Execute!</summary>

```python
class TemperatureNode(AbstractNode):
    def __init__(self, my_temp: float):
        self.my_temp = my_temp
        self.max_seen = my_temp
        self.children_responses = 0
        self.total_children = len(self.getChildren())
        self.has_broadcasted = False

    def run(self):
        """
        Entry point: Leaf nodes initiate the Convergecast.
        """
        if self.isLeaf():
            # I have no children to wait for.
            # Send my temperature up to my parent immediately.
            self.sendToParent(self.my_temp)
        
        # If I am not a leaf, I do nothing yet. 
        # I must wait for messages from all my children.

    def receiveFromChild(self, child_max: float):
        """
        Triggered when a child node sends its local maximum.
        """
        # Update the highest temperature seen so far
        self.max_seen = max(self.max_seen, child_max)
        self.children_responses += 1

        # Check if I've heard from every branch below me
        if self.children_responses == self.total_children:
            if not self.isRoot():
                # Pass the winner up to the parent
                self.sendToParent(self.max_seen)
            else:
                # I am the Root! I now know the Global Maximum.
                print(f"Global Max Temperature Found: {self.max_seen}")
                # Phase 2: Tell everyone the result
                self.broadcastToChildren(self.max_seen)

    def receiveFromParent(self, global_max: float):
        """
        Phase 2: The result travels back down the branches.
        """
        self.max_seen = global_max
        print(f"Node updated with Global Max: {self.max_seen}")
        
        # Forward the final result to all children
        self.broadcastToChildren(global_max)

```
</details>
<BR>

### The "Firing Squad" Synchronization

The Firing Squad problem requires a linear network of asynchronous nodes to execute a specific action simultaneously despite the lack of a global clock. 
The challenge lies in coordinating this synchronized "fire" command using only local message passing, which must account for the inherent time delays of 
signal propagation across the chain.

<details><summary markdown="span">Execute!</summary>

```python


```
</details>
<BR>


### Termination Detection

In a distributed system where a "Manager" node initiates computations that can trigger subsequent tasks across various nodes, the challenge is determining the exact
moment the entire process has ceased. The problem requires a mechanism to track both active node states and "in-flight" messages to ensure no further computation
will be triggered before the Manager declares the system idle.

<details><summary markdown="span">Execute!</summary>

```python

```
</details>
<BR>



