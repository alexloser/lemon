// Make random password for unix
package main

import (
	"flag"
	"math/rand"
	"os"
	"time"
)

var CHARSET = [79]byte{
	'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
	'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
	'0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
	'#', ':', '@', '!', '+', '-', '*', '/', '~', '$', ')', '(', ']', '[', '}', '{', '?',
}

var gen = rand.New(rand.NewSource(time.Now().UnixNano()))

func random() int {
	return int(gen.Float64() * 10000.0)
}

func main() {
	var n, d int
	flag.IntVar(&d, "d", 12, "length of the password")
	flag.IntVar(&n, "n", 1, "total number of passwords to make")
	flag.Parse()

	if n < 1 || d < 1 {
		println("Error Argument!")
		os.Exit(-1)
	}

	for i := 0; i < random(); i++ {
		random()
	}

	for i := 0; i < n; i++ {
		w := []byte{}
		for j := 0; j < d; j++ {
			w = append(w, CHARSET[random()%len(CHARSET)])
		}
		println(string(w))
	}
}
