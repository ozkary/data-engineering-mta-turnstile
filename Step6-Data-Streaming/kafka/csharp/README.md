# Using .NET Core SDK

To build and run a .NET Core application, follow these steps:

1. **Install .NET Core SDK:**
   Ensure you have the .NET Core SDK installed on your machine. You can download it from the [.NET Core downloads page](https://dotnet.microsoft.com/download).

2. **Create a .NET Core Project:**
   Create a new .NET Core project using the `dotnet new` command. For example:
   ```bash
   dotnet new console -n MyKafkaConsumerApp

   # or do not provide a dir name to create the files in the current folder

   dotnet new console
   ```

3. **Navigate to Project Directory:**
   Change to the project directory:
   ```bash
   cd MyKafkaConsumerApp
   ```

4. **Restore Dependencies:**
   Restore the project dependencies using the `dotnet restore` command:
   ```bash
   dotnet restore
   ```

5. **Edit and Write Your Code:**
   Open the project in your preferred code editor and write the necessary code for your Kafka consumer application.

6. **Build the Project:**
   Build the project using the `dotnet build` command:
   ```bash
   dotnet build
   ```

7. **Run the Application:**
   Run the application using the `dotnet run` command:
   ```bash
   dotnet run
   ```

8. **Add the confluent NuGet Package:**
   
   ```bash
   dotnet add package Confluent.Kafka
   ```


Ensure that your Kafka consumer code is appropriately written in the `.cs` files in your project before building and running.

If you have specific code you'd like assistance with or encounter any issues during this process, feel free to share, and I'll be glad to help!