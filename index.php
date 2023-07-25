<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Monitoring Sistem Parkir Uper</title>
    <script src="script.js" defer></script>

    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f0f0f0;
        }
        body h1 {
            text-align: center;
            margin: 0;
            padding: 20px;
            color: white;
            background-color: #696969;
        }

        table {
            width: 80%;
            margin: 30px auto;
            border-collapse: collapse;
            border: 1px solid #ccc;
            background-color: #fff;
        }

        th, td {
            padding: 10px;
            text-align: center;
            border-bottom: 1px solid #ccc;
        }

        th {
            background-color: #f2f2f2;
        }

        tr:nth-child(even) {
            background-color: #f2f2f2;
        }

        tr:hover {
            background-color: #e0e0e0;
        }
    </style>
    
</style>
</head>
<body>
    <h1>Data dari Database</h1>
    <table>
        <tr>
            <th>ID</th>
            <th>Data Kendaraan</th>
            <th>Identifikasi</th>
            <th>Status</th>
            <th>Waktu Masuk</th>
            <th>Waktu Keluar</th>
        </tr>
        <?php
        // Menghubungkan ke database
        $koneksi = mysqli_connect("127.0.0.1", "root", "", "sistemparkiruper");

        // Memeriksa koneksi
        if (mysqli_connect_errno()) {
            echo "Koneksi ke database gagal: " . mysqli_connect_error();
        }

        // Mengambil data dari database
        $query = "SELECT id, filename, image_data, status, timestamp FROM images";
        $result = mysqli_query($koneksi, $query);

        // Menampilkan data dalam tabel
        while ($row = mysqli_fetch_assoc($result)) {
            echo "<tr>";
            echo "<td>" . $row['id'] . "</td>";
            echo "<td>" . $row['filename'] . "</td>";
            echo '<td> <img src="data:image/png;base64,'.base64_encode($row['image_data']).'"/> </td>';
            echo "<td>" . $row['status'] . "</td>";

            // Mengambil nilai timestamp dari hasil query database
            $timestamp = $row['timestamp'];
            $formatted_timestamp = date('Y-m-d H:i:s', strtotime($timestamp));
            echo "<td>" . $formatted_timestamp . "</td>";
            echo "</tr>";
        }

        // Menutup koneksi
        mysqli_close($koneksi);
        ?>
    </table>
</body>
</html>