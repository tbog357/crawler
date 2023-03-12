package main

import (
	"fmt"
	"time"
)

func say(s string) {
	for i := 0; i < 5; i++ {
		time.Sleep(100 * time.Millisecond)
		fmt.Println(s)
	}
}

func sum(s []int, c chan int) {
	sum := 0
	for _, v := range s {
		sum += v
	}
	c <- sum // send sum to c
}

func fibonacci(n int, c chan int) {
	x, y := 0, 1
	for i := 0; i < n; i++ {
		c <- x
		x, y = y, x+y
	}
	// sender can close the channel to indicate that no more values
	// will be sent. Receivers can test whether a channel has been closed

	close(c)
}

func fibonacci_select(c, quit chan int) {
	x, y := 0, 1
	for {
		select {
		// select blocks until one of it cases can run,
		// then it executes that case.
		// Choose one at random if multiple are ready
		// Use default in select if no other case is ready
		// in default case dont send or receive from the same channel used in other cases, it would caused blocking
		case c <- x:
			x, y = y, x+y
		case <-quit:
			fmt.Println("quit")
			return
		}
	}
}

type Tree struct {
	Left  *Tree
	Value int
	Right *Tree
}

func equivalent_binary_tree() {
	// check 2 binary trees have the same storing sequence in array representation

}

// goroutine is a lightweight thread managed by the Go runtime
// goroutine run in the same address space, so access to shared memory must be synchronized.
// channels are designed for goroutine
// recieving <- channel <- sending

// send and receives block until the other side is ready
// without explicit locks or condition variables

func notmain() {
	go say("world")
	say("hello")

	s := []int{7, 2, 8, -9, 4, 0}

	// define the second argument to initlize a buffered channel
	c := make(chan int)
	go sum(s[:len(s)/2], c)
	go sum(s[len(s)/2:], c)

	x, y := <-c, <-c // receive from c
	fmt.Println(x, y, x+y)
	// close the channel ?
	// channel can be buffered
	// sends to a buffered channel block only when the buffer is full
	// receives block when the buffer is empty

	// channel act as first in first out queue

	ch := make(chan int, 3)
	ch <- 1
	ch <- 2
	ch <- 3 // all goroutines are asleep - deadlock!
	fmt.Println(<-ch)
	fmt.Println(<-ch)
	fmt.Println(<-ch)
	// in underfill case, it will ignore remain values

	fib_chan := make(chan int, 10)
	go fibonacci(cap(fib_chan), fib_chan)
	for i := range fib_chan {
		fmt.Println(i)
	}
	// Closing is only necessary when the receiver must be told there
	// are no more values coming, such as to terminate a range loop
	fib_select_chan := make(chan int)
	quit := make(chan int)

	go func() {
		for i := 0; i < 10; i++ {
			fmt.Println(<-fib_select_chan)
		}
		quit <- 0
	}()
	fibonacci_select(fib_select_chan, quit)

	tick := time.Tick(100 * time.Millisecond)
	boom := time.After(500 * time.Millisecond)

	for {
		select {
		case <-tick:
			fmt.Println("tick.")
		case <-boom:
			fmt.Println("boom")
			return
		default:
			fmt.Println("        .")
			time.Sleep(50 * time.Millisecond)

		}
	}
}
