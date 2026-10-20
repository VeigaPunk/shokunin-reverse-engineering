(module
  (import "env" "get" (func $get (param i32) (result i32)))
  (func (export "old_api") (param $x i32) (result i32)
    local.get $x
    call $get)
  (func (export "stable") (result i32)
    i32.const 7))
