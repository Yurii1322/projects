#!/bin/bash

sudo yum update -y

sudo yum install -y httpd php stress

sudo rm -f /var/www/html/index.html

echo '<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Welcome to Our Server</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background-color: #f4f4f4;
            margin: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }

        .container {
            text-align: center;
            padding: 20px;
            background-color: #fff;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }

        h1 {
            color: #333;
        }

        p {
            color: #555;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Welcome to Our Server!</h1>
        <p>Public IP Address of the server: <?php echo file_get_contents("https://ipinfo.io/ip"); ?></p>
    </div>
</body>
</html>' | sudo tee /var/www/html/index.php > /dev/null

sudo systemctl restart httpd
