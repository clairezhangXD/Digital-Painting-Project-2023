from __future__ import annotations
from abc import ABC, abstractmethod
from layer_util import Layer
from data_structures.queue_adt import CircularQueue
from data_structures.stack_adt import ArrayStack
from data_structures.bset import BSet
from data_structures.array_sorted_list import ArraySortedList
from data_structures.sorted_list_adt import ListItem



class LayerStore(ABC):

    def __init__(self) -> None:
        pass

    @abstractmethod
    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.
        Returns true if the LayerStore was actually changed.
        """
        pass

    @abstractmethod
    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.
        """
        pass

    @abstractmethod
    def erase(self, layer: Layer) -> bool:
        """
        Complete the erase action with this layer
        Returns true if the LayerStore was actually changed.
        """
        pass

    @abstractmethod
    def special(self):
        """
        Special mode. Different for each store implementation.
        """
        pass


class SetLayerStore(LayerStore):
    """
    Complexity of class methods are O(1), unless otherwise specified
    """

    def __init__(self):
        """
        Description: Initialise layer store layer and special boolean
        """
        self.layer = None
        self.is_special = False  # special() not called

    def add(self, layer: Layer) -> bool:
        """
        Description: Add single layer to the store.

        Args:
        - layer: one of the layer types in layers.py

        Returns:
        - True if LayerStore was actually changed
        """
        if self.layer != layer:
            self.layer = layer  # setting new layer
            return True
        else:
            return False  # layer added is same

    def get_color(self, start: tuple[int, int, int], timestamp: int, x: int, y: int) -> tuple[int, int, int]:
        """
        Description: applies layer stored in grid cell/pixel to the color of that pixel (and applies special if called)
         to get resulting color

        Args:
        - start: initial color of pixel
        - timestamp: timestamp of pixel
        - x: x coordinate of pixel
        - y: y coordinate of pixel

        Returns:
        - colour this square should show, given the current layers

        Complexity:
        - Best case: O(1), when no layer applied, so return start, which takes constant time
        - Worst case: O(apply), other elementary operations/assignments/returns are constant time.
        """
        if self.layer == None:  # no layer stored
            color = start  # color is white
        else:
            color = self.layer.apply(start, timestamp, x, y)  # apply layer to input to retrieve resulting color

        # special inverts after layer applied
        if self.is_special:
            color = (255-color[0], 255-color[1], 255-color[2])

        return color

    def erase(self, layer: Layer) -> bool:
        """
        Description: Remove single layer in store

        Args:
        - layer: one of the layer types in layers.py

        Returns:
        - True if LayerStore was actually changed
        """
        if self.layer != None:
            self.layer = None  # removes layer
            return True
        else:
            return False  # already no layer

    def special(self):
        """
        Description: Allows get_color to invert the colour output
        """
        self.is_special = not self.is_special  # special() called so switches to True


class AdditiveLayerStore(LayerStore):
    """
    Complexity of class methods are O(1), unless otherwise specified
    """

    CAPACITY = 2000  # assuming max 20 layers*100 = 2000

    def __init__(self) -> None:
        """
        Description: Initialise queue that stores layers
        """
        # Worst case time complexity: O(1), since CAPACITY is a fixed integer class variable,
        # so we know CAPACITY is not asymptotic
        self.store = CircularQueue(AdditiveLayerStore.CAPACITY)

    def add(self, layer: Layer) -> bool:
        """
        Description: Add layer to rear of the store

        Args:
        - layer: one of the layer types in layers.py

        Returns:
        - True, since layer is always added when called
        """
        self.store.append(layer)
        return True

    def get_color(self, start: tuple[int, int, int], timestamp: int, x: int, y: int) -> tuple[int, int, int]:
        """
        Description: applies store layers in order of queue (FIFO) stored in grid cell/pixel to
        the color of that pixel to get resulting color

        Args:
        - start: initial color of pixel
        - timestamp: timestamp of pixel
        - x: x coordinate of pixel
        - y: y coordinate of pixel

        Returns:
        - colour this square should show, given the current layers

        Complexity:
        - Best case: O(1), if queue is empty, then starting color is returned, which takes constant time
        - Worst case: O(n*apply), where n is the length of the queue. Have to apply each layer, which means number of
         iterations depends on this input size n.
        """
        # check if queue empty, return white layer (start)
        color = start
        if self.store.is_empty():
            pass
        else:
            for i in range(len(self.store)):
                oldest_layer = self.store.serve()  # oldest layer is deleted from queue
                color = oldest_layer.apply(color, timestamp, x, y)  # deleted layer is applied first
                self.store.append(oldest_layer)
        return color

    def erase(self, layer: Layer) -> bool:
        """
        Description: Removes front of store

        Args:
        - layer: one of the layer types in layers.py

        Returns:
        - True if LayerStore was actually changed
        """
        if self.store.is_empty():
            return False
        else:
            self.store.serve()
            return True

    def special(self):
        """
        Description: Reverse the order of current layers (first becomes last, etc.)

        Time complexity:
        Best case: O(1), when the store queue is empty, the stack and new store queue will remain empty too
        Worst case: O(n), where n is the len(store), as it will take len(store) iterations to move all layers
        in store queue to the stack. The same number of iterations is required to move the stack layers
         to new store queue
        """
        # Worst case time complexity: O(1), since CAPACITY is a fixed integer class variable,
        # so we know CAPACITY is not asymptotic
        stack = ArrayStack(AdditiveLayerStore.CAPACITY)
        new_store = CircularQueue(AdditiveLayerStore.CAPACITY)

        # Worst case time complexity: O(len(store))
        for i in range(self.store.length):
            stack.push(self.store.serve())  # serve oldest layer and push to temporary stack

        # Worst case time complexity: O(len(store))
        while not stack.is_empty():
            new_store.append(stack.pop())  # pop top of stack, which was self.store's newest layer and append to new

        self.store = new_store  # new becomes self.store


class SequenceLayerStore(LayerStore):
    """
    Complexity of class methods are O(1), unless otherwise specified
    """
    NUM_LAYERS = 9

    def __init__(self) -> None:
        self.store_applied = BSet()

        # Worst case time complexity: O(1), since NUM_LAYERS is a fixed integer class variable,
        # so we know NUM_LAYERS is not asymptotic
        self.store_layers = ArraySortedList(SequenceLayerStore.NUM_LAYERS)

    def add(self, layer: Layer) -> bool:
        """
        Description: Ensures layer is applied and added to list
        
        Args: 
        - layer: one of the layer types in layers.py
        
        Returns: 
        - True if LayerStore was actually changed
        
        Time Complexity:
        - Best case: O(1), if item is already applying. Calls to __contains__, which uses bitewise operations
         that take constant time to do the check
        - Worst case: O(add), where add is the method for adding the layer item to the array sorted list, not
        marking the layer as applying in the bitvector set, which takes constant time.
        """

        # add layers in store_applied to list in order
        item = layer.index+1  # index starts from 0, but item in sets start from 1

        if item in self.store_applied:
            return False
        else:

            # O(1)
            self.store_applied.add(item)  # layer is 'applying'

            layer_item = ListItem(layer, layer.name)  # add name as key, to sort in lexicographical order

            # Worst case time complexity: O(add), requires shuffling, so run time depends on this
            self.store_layers.add(layer_item)  # layer will be added to 'applying' layers list
            return True

    def get_color(self, start: tuple[int, int, int], timestamp: int, x: int, y: int) -> tuple[int, int, int]:
        """
        Description: Based on applying layers and their lexicographical order, layers are applied to the grid cell
        to return resulting color

        Args:
        - start: initial color of pixel
        - timestamp: timestamp of pixel
        - x: x coordinate of pixel
        - y: y coordinate of pixel

        Returns:
        - colour this square should show, given the current layers

        Time Complexity:
        - Best case: O(1), when no layers are applying, start is returned, which takes constant time
        - Worst case: O(len(store_layers)*apply), will need to apply each layer stored in the array sorted list,
        so time complexity depends on the time complexity of apply, and how many times it runs depends
        on len(store_layers)
        """
        color = start
        if self.store_applied.is_empty():  # check if no layers 'applying'
            pass
        else:

            # Worst = best case: O(1), as NUM_LAYERS is a constant integer, so iterations does not depend on
            # any input size, but on this constant
            for i in range(SequenceLayerStore.NUM_LAYERS):  # iterate through all layer indices in order
                item = i+1  # layer item is layer.index+1

                if item in self.store_applied:  # check if layer 'applying'

                    # Worst case: O(len(store_layers)), number of iterations depends on this input size of number of
                    # layers in the store layers list
                    for j in range(len(self.store_layers)):  # iterate 'applying' layers
                        current_layer = self.store_layers[j]

                        if current_layer.value.index == i:  # check if 'applying' layer matches layer.index

                            # O(apply)
                            color = current_layer.value.apply(color, timestamp, x, y)

        return color

    def erase(self, layer: Layer) -> bool:
        """
        Description: Ensures layer is 'not applying' and is deleted from array sorted list of layers

        Args:
        - layer: one of the layer types in layers.py

        Returns:
        - True if LayerStore was actually changed
        
        Time complexity:
        - best case: O(1), when item is 'not applying' already, as checked by __contains__, which takes constant time
        to check
        - worst case: O(len(store_layers)+delete_at_index) = O(Max{len(store_layers),delete_at_index}) 
        When layer item is 'applying', a number of iterations occurs to find the index of the layer within the 
        list, then once it is found, it is deleted. So, only 1 layer is deleted in the process.
        The number of iterations depends on len(store_layers), so it is an input size that affects
        run time. The time complexity of delete_at_index could be greater or smaller than len(store_layers), therefore
        the overall worst case time complexity is the greater of the two 
        """
        item = layer.index+1  # index starts from 0, but item in sets start from 1

        if item in self.store_applied:
            # make layer "not applying"
            self.store_applied.remove(item)

            # delete layer in list
            # Worst case: O(len(store_layers)), number of iterations depends on this input size of number of
            # layers in the store layers list
            for i in range(len(self.store_layers)):
                current_layer = self.store_layers[i]
                if current_layer.value.index == item-1:

                    # O(delete_at_index)
                    self.store_layers.delete_at_index(i)

            return True
        else:
            return False

    def special(self):
        """
        Description: Removes median name of applied layers

        Time complexity:
        - best case: O(1), when no layers are 'applying', so store_layers is empty, so delete_at_index() is not called
        - worst case: O(delete_at_index), when store_layers is not empty,
         so there are layers 'applying', so 1 layer will be deleted and run time will depend on
         time complexity of delete_at_index operation
        """
        if self.store_layers.is_empty():
            pass
        else:

            # Find median index
            # Worst = best case time complexity: O(1). len(store_layers) is an integer, and integer
            # comparisons take constant time. Elementary operations on integers also take constant time, so overall
            # time complexity is constant time
            if len(self.store_layers) == 1:  # only 1 layer
                median_index = 0
            elif len(self.store_layers) % 2 != 0:  # odd number of layers
                median_index = int(len(self.store_layers) // 2)
            else:  # even number of layers
                median_index = int((len(self.store_layers) / 2)-1)  # -1 from indices to pick smaller median name

            self.store_layers.delete_at_index(median_index)  # removes median name


