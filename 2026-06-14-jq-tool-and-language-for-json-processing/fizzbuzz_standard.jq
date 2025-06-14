range(1; 101) |
  if . % 15 == 0 then
    "FizzBuzz"
  elif . % 3 == 0 then
    "Fizz"
  elif . % 5 == 0 then
    "Buzz"
  else
    .
  end
