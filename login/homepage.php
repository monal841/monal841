<?php
session_start();
include("connect.php");

?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Homepage</title>
    <link rel="stylesheet" href="style2.css">
</head>
<body>
    <div class="container" style="text-align:center; padding: 5%; margin-top: 50px;">
        <h1 class="welcome-title">Welcome Back!</h1>
        <p class="greeting-message">
            Hello <?php 
            if(isset($_SESSION['email'])){
                $email = $_SESSION['email'];
                $query = mysqli_query($conn, "SELECT users.* FROM `users` WHERE users.email='$email'");
                while ($row = mysqli_fetch_array($query)) {
                    echo $row['firstName'] . ' ' . $row['lastName'];
                }
            }
            ?> :)
        </p>
        
        <form method="POST" action="">
            <div class="input-group">
                <label for="category">Choose a category for image generation:</label>
                <select name="category" id="category">
                    <option value="">Select a category</option>
                    <option value="nature">Nature</option>
                    <option value="city">City</option>
                    <option value="abstract">Abstract</option>
                    <option value="animals">Animals</option>
                    <option value="ocean">Ocean</option>
                    <option value="landscape">Landscape</option>

                    <!-- Add more predefined categories as needed -->
                </select>
                <label for="custom_category">or enter a new category:</label>
                <input type="text" name="custom_category" id="custom_category" placeholder="New category (optional)">
            </div>
            <input type="submit" class="btn" value="Generate Image">
        </form>

        <?php
        // Handle image generation when form is submitted
        if ($_SERVER['REQUEST_METHOD'] == 'POST') {
            $category = isset($_POST['category']) && $_POST['category'] !== '' ? $_POST['category'] : null;
            $customCategory = isset($_POST['custom_category']) && $_POST['custom_category'] !== '' ? trim($_POST['custom_category']) : null;

            // Use custom category if provided
            if ($customCategory) {
                $category = $customCategory;
            }

            if ($category) {
                // Call the Python API to generate an image based on the category
                $url = 'http://127.0.0.1:5000/generate-image'; // Update with your actual Flask API endpoint
                $data = json_encode(array("category" => $category));

                // Initialize CURL session
                $ch = curl_init($url);
                curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
                curl_setopt($ch, CURLOPT_POST, true);
                curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type: application/json'));
                curl_setopt($ch, CURLOPT_POSTFIELDS, $data);

                // Execute CURL and get response
                $response = curl_exec($ch);
                curl_close($ch);

                // Decode the response
                $responseData = json_decode($response, true);

                // Check if the response contains an image URL
                if (isset($responseData['image_url'])) {
                    echo '<div class="image-container">';
                    echo '<h2>Generated Image:</h2>';
                    echo '<img src="' . $responseData['image_url'] . '" alt="Generated Image" style="max-width: 100%; height: auto; border-radius: 10px; margin-top: 20px;">';
                    echo '</div>';
                } else {
                    echo '<p class="error-message">Error: ' . (isset($responseData['error']) ? $responseData['error'] : 'Image generation failed.') . '</p>';
                }
            } else {
                echo '<p class="error-message">Please select or enter a category.</p>';
            }
        }
        ?>
        
        <div class="logout">
            <a href="logout.php" class="btn logout-btn">Logout</a>
        </div>
    </div>
</body>
</html>
