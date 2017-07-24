import Network.Socket hiding (send,recv)
import Network.Socket.ByteString
import Data.ByteString.Char8 (pack,unpack)
import Control.Monad
import Control.Concurrent
import Control.Concurrent.Chan

main = do
  sock <- socket AF_INET Stream 0
  setSocketOption sock ReuseAddr 1
  bind sock (SockAddrInet 4242 iNADDR_ANY)
  listen sock 2
  chan <- newChan
  forkIO $ forever $ loop sock chan
  forever $ readChan chan >>= putStr

loop sock chan = do
  conn <- accept sock
  forkIO $ handleConn conn chan

handleConn (sock,_) chan = do
  let write = send sock . pack
      broadcast = writeChan chan
  write "Username: "
  name <- liftM (strip . unpack) $ recv sock 20
  write $ "Welcome, " ++ name ++ "!\n"
  broadcast $ "User '" ++ name ++ "' logged in.\n"

  broadcaster <- dupChan chan
  --recieve
  let isByMe = commonStart (name)
  forkIO . forever $ do
    line <- readChan broadcaster
    if not $ isByMe line then
      send sock $ pack line
    else
      return 0
  --send
  while $ do
    line <- fmap unpack $ recv sock 100
    if (strip line) /= "quit" then do
      broadcast $ name ++ ": " ++ line
      return True
    else do
      close sock
      return False

commonStart "" _ = True
commonStart _ "" = True
commonStart (x:xs) (y:ys) = if x /= y then False else commonStart xs ys

while action = do
  continue <- action
  if continue then while action else return ()

strip "" = ""
strip ('\r':xs) = strip xs
strip ('\n':xs) = strip xs
strip (x:xs) = x:strip xs
