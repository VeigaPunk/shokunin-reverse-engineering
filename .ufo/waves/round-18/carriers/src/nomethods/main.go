// Round-18 synthetic Go carrier: the same program with an UNNAMED map type
// and free functions, so the program declares no map type with methods.
// Built, never executed by the lane; REA analyzes a copy statically.
package main

import (
	"fmt"
	"os"
	"sort"
)

func keys(c map[string]int) []string {
	k := make([]string, 0, len(c))
	for s := range c {
		k = append(k, s)
	}
	sort.Strings(k)
	return k
}

func str(c map[string]int) string { return fmt.Sprint(keys(c)) }

func main() {
	c := map[string]int{}
	for _, a := range os.Args[1:] {
		c[a]++
	}
	fmt.Println(str(c), len(c))
}
