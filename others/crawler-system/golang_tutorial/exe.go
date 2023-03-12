package main

import (
	"fmt"

	"golang.org/x/tour/tree"
)

// Walk walks the tree t sending all values
// from the tree to the channel ch.
func Walk(t *tree.Tree, ch chan int) {
	// Go left
	if t.Left != nil {
		Walk(t.Left, ch)
	}

	// Root
	ch <- t.Value

	// Go right
	if t.Right != nil {
		Walk(t.Right, ch)
	}
}

// Same determines whether the trees
// t1 and t2 contain the same values.
func Same(t1, t2 *tree.Tree) bool {
	ch1 := make(chan int)
	ch2 := make(chan int)
	go Walk(t1, ch1)
	go Walk(t2, ch2)

	var i int
	for i = 0; i < 10; i++ {
		if <-ch1 != <-ch2 {
			return false
		}
	}
	return true
}

// func main() {
// 	// when using range syntax, the channel must be closed
// 	fmt.Println(Same(tree.New(1), tree.New(2)))
// }
