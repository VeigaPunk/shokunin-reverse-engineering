// Round-18 synthetic Go carrier: one named map type WITH methods.
// Built, never executed by the lane; REA analyzes a copy statically.
package main

import (
	"fmt"
	"os"
	"sort"
)

// Counts is a named map type with methods, so its type descriptor carries
// uncommon (method) information after the map-type struct.
type Counts map[string]int

func (c Counts) Keys() []string {
	k := make([]string, 0, len(c))
	for s := range c {
		k = append(k, s)
	}
	sort.Strings(k)
	return k
}

func (c Counts) String() string { return fmt.Sprint(c.Keys()) }

func main() {
	c := Counts{}
	for _, a := range os.Args[1:] {
		c[a]++
	}
	var s fmt.Stringer = c
	fmt.Println(s.String(), len(c))
}
