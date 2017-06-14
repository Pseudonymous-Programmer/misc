import Text.ParserCombinators.Parsec hiding (choice)
import Data.Random.Extras hiding (sample)
import Data.Random.RVar
import Data.Random 
import Data.List.Split
import System.Environment

data Rule = Rule String [String] deriving Show

cfg :: Parser [Rule]
cfg = do
  many (char '\n') --munch newlines
  result <- many rule
  many (char '\n')
  eof
  return result

rule :: Parser Rule
rule = do
  name <- many letter
  string ":\n"
  subrules <- many subrule
  many (char '\n')
  return $ Rule name subrules
  
subrule :: Parser String
subrule = do
  (string "\t") <|> (many (char ' '))
  result <- many1 (noneOf "\n")
  char '\n'
  return result
  
parseCFG :: String -> Either ParseError [Rule]
parseCFG input = parse cfg "???" input
  
find :: String -> [Rule] -> [String]
find _ [] = []
find x (Rule key value:xs) = if x == key then value else find x xs

excludeOther :: [a] -> Bool -> [a]
excludeOther [] _ = []
excludeOther (x:xs) True = excludeOther xs False
excludeOther (x:xs) False = x:excludeOther xs True

splice :: [a] -> [a] -> [a]
splice [] x = x
splice x [] = x
splice (x:xs) (y:ys) = x:y:splice xs ys

runCFG :: [String] -> [Rule] -> RVar String
runCFG subrules rules = do
  chosen <- choice subrules
  let split = splitOn "|" chosen
      evens = excludeOther split False
      odds = excludeOther split True
  odds' <- mapM ((flip runCFG rules) . (flip find rules)) odds
  return $ foldl1 (++) $  splice evens odds'
  
main = do
  file <- fmap head getArgs
  input <- readFile file
  case parseCFG input of
    (Left err) -> print err
    (Right rules) -> sample (runCFG (find "main" rules) rules) >>= putStrLn
