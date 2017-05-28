data StackMember a = Func (a -> StackMember a) | Value a
instance (Show a) => Show (StackMember a) where
  show (Value v) = show v
  show _ = "???"
type Stack a = [StackMember a]

compress :: Stack a -> Stack a
compress [] = []
compress ((Func f):(Value v):xs) = compress ((f v):xs)
compress ((Func f):xs) = compress ((Func f):compress xs)
compress x = x

liftS1 :: (a -> a) -> StackMember a
liftS1 f = Func (\x -> Value $ f x)

liftS2 :: (a -> a -> a) -> StackMember a
liftS2 f = Func (\x -> (Func (\y -> Value $ f x y)))

addS = liftS2 (+)
divS = liftS2 (/)
subS = liftS2 (-)
mulS = liftS2 (*)
powS = liftS2 (**)
logS = liftS2 logBase
piS = Value pi
cosS = liftS1 cos
sinS = liftS1 sin
tanS = liftS1 tan

parse :: [String] -> Stack Double
parse ("+":xs) = addS:parse xs
parse ("-":xs) = subS:parse xs
parse ("/":xs) = divS:parse xs
parse ("*":xs) = mulS:parse xs
parse ("^":xs) = powS:parse xs
parse ("logBase":xs) = logS:parse xs
parse ("pi":xs) = piS:parse xs
parse ("cos":xs) = cosS:parse xs
parse ("sin":xs) = sinS:parse xs
parse ("tan":xs) = tanS:parse xs
parse (x:xs) = (Value (read x)):parse xs
parse [] = []

main = do
  putStr "calc.hs> "
  input <- getLine
  let parsed = parse $ words input
      ([result]) = compress parsed
  print result
  main
