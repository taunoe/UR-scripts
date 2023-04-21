// See https://aka.ms/new-console-template for more information
// NET 6
// Server program
// Tauno Erik
// Started: 17.04.2023
// Edited:  21.04.2023

using System;
using System.Net;
using System.Net.Sockets;
using System.Text;


// The IP address of the server (the PC on which this program is running)
string server_ip = "192.168.98.23"; // "127.0.0.1"
int server_port  = 50000; // 21

// The following names are used in the PolyScope script
// UR sends this command when it asks new pose
const string ur_cmd_new_pose = "newpose";

Console.WriteLine("Server IP Address: " + server_ip);
IPAddress ipAddress = IPAddress.Parse(server_ip);                   // Create the IP address
Console.WriteLine("Server Port: " + server_port);
TcpListener tcpListener = new TcpListener(ipAddress, server_port);  // Create the tcp Listener
tcpListener.Start();                                                // Start listening

// Keep on listening forever
while (true)
{
    TcpClient tcpClient = tcpListener.AcceptTcpClient();        // Accept the client
    Console.WriteLine("UR connected");                          // "Accepted new client"
    NetworkStream stream = tcpClient.GetStream();               // Open the network stream
    while (tcpClient.Client.Connected)
    {
        // Create a byte array for the available bytes
        byte[] arrayBytesRequest = new byte[tcpClient.Available];
        // Read the bytes from the stream
        int nRead = stream.Read(arrayBytesRequest, 0, arrayBytesRequest.Length);

        if (nRead > 0)
        {
            // Convert the byte array into a string
            string sMsgRequest = ASCIIEncoding.ASCII.GetString(arrayBytesRequest);
            Console.WriteLine("Received message: " + sMsgRequest);
            string pose = string.Empty;

            if (sMsgRequest.Substring (0,7).Equals(ur_cmd_new_pose))
            {
                pose = "(-0.05, -0.25, 0.15, -0.01, 3.11, 0.38)";
            }

            if (pose.Length > 0)
            {
                Console.WriteLine("Sending pose: " + pose);
                // Convert the point into a byte array
                byte[] arrayBytesAnswer = ASCIIEncoding.ASCII.GetBytes(pose+'\n');
                // Send the byte array to the client
                stream.Write(arrayBytesAnswer, 0, arrayBytesAnswer.Length);
            }
        }
        else
        {
            if (tcpClient.Available == 0)
            {
                Console.WriteLine("UR closed the connection.");
                // No bytes read, and no bytes available, the client is closed.
                stream.Close();
            }
        }
    }
}
