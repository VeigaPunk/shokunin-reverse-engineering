(module
  (import "env" "get" (func $get (param i32 i64) (result i64)))
  (func (export "new_api") (param $x i32) (result i32)
    local.get $x
    i64.const 1
    call $get
    i32.wrap_i64)
  (func (export "stable") (result i32)
    i32.const 7))
