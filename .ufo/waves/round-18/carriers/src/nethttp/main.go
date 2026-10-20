// Round-18 synthetic Go carrier: stdlib named map types with methods and
// 40-byte Swiss slots (http.Header, url.Values, textproto.MIMEHeader are
// map[string][]string), the shapes present in /usr/bin/aether.
// Built, never executed by the lane; REA analyzes a copy statically.
package main

import (
	"fmt"
	"net/http"
	"net/textproto"
	"net/url"
	"os"
)

func main() {
	h := http.Header{}
	m := textproto.MIMEHeader{}
	v := url.Values{}
	for _, a := range os.Args[1:] {
		h.Add("X-Arg", a)
		m.Add("X-Arg", a)
		v.Add("arg", a)
	}
	fmt.Println(len(h), len(m), v.Encode())
}
