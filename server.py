#Name : Nam Nguyen
#UTA ID: 1001823561

#Immport necessary modules that facilitates the process of making this project
from socket import *
from threading import *
import os

#Initialize the function that handles connection requests and client/connection socket
def handleRequest(clientSocket):
    #Receive and decode the data received from the client's request
    requestData = clientSocket.recv(1024).decode('utf-8')
    print(requestData)

    #Split the requested data into lines 
    requestLines = requestData.split()
    request = ''
    #Extract the requested file if it is detected within the client's request
    if len(requestLines) > 1 and len(requestLines[1]) > 1:
        request = requestLines[1][1:]
    print(request)

    #If the client requests for an existing webpage (in this case, it's 'image.html')
    # then web server process will fetch the html file from the file system, compose
    # the http response, and send it back to the browser
    if request == 'image.html':
        file = open(os.path.realpath(os.path.dirname(__file__)) + '\\' + request, 'rb')
        responseMessage = b"HTTP/1.1 200 OK \r\nContent-Type: text/html\r\n\r\n" + file.read()
        file.close()

    #This reads and sends the image file as an http response if the user requests it
    #and it also fetches the image to the image.html file as the previous conditional
    # if only contains text/html within the webpage 
    elif request == 'cat.jpg':
        file = open(os.path.realpath(os.path.dirname(__file__)) + '\\' + request, 'rb')
        responseMessage = b"HTTP/1.1 200 OK \r\nContent-Type:image/jpeg\r\n\r\n" + file.read()
        file.close()

    #If the client requests for page1.html, send a 301 Error to the webpage and redirect 
    # the url to /page2.html instead 
    elif request == 'page1.html':
        responseMessage = b"HTTP/1.1 301 Moved Permanently \r\nLocation: /page2.html\r\n\r\n"       

    elif request == 'page2.html':
        file = open(os.path.realpath(os.path.dirname(__file__)) + '\\' + 'page2.html', 'rb')
        responseMessage = b"HTTP/1.1 200 OK \r\n\r\n" + file.read()
        file.close()
    #If the client requests for any html file that is not specified above, then the web server
    # process will send a 404 Error and fetch the customized 404.html file from the file system to 
    # show the error on the webpage
    else:
        file = open(os.path.realpath(os.path.dirname(__file__)) + '\\' + '404.html', 'rb')
        responseMessage = b"HTTP/1.1 404 File Not Found \r\nError 404: file not found\r\n\r\n" + file.read()
        file.close()

    #Send the response to the clients requesting and terminate the connection once a request is finished
    clientSocket.sendall(responseMessage)
    clientSocket.close()
    print('Connection terminated')

#The main function of the script
if __name__ == '__main__':

    #Initialize a new variable to create a server socket
    serverSocket = socket(AF_INET, SOCK_STREAM)
    #Bind the established server socket to the localhost and 8080 as new connections
    serverSocket.bind(('localhost', 8080))
    #Set the server socket to listen to new connections 
    serverSocket.listen(1)

    print('Server listening in port 8080')

    #Set up a loop to accept and handle incoming requests from clients
    while True:
        clientSocket, addr = serverSocket.accept()
        #Create a new thread to handle concurrent client requests every time a new connection
        # is created
        clientHandler = Thread(target = handleRequest, args = (clientSocket,))
        clientHandler.start()

