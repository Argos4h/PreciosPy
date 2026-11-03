Add-Type -AssemblyName System.Drawing

$srcPath = "C:\Users\munic\Desktop\PreciosPy\docs\preciospy_icon_minimalist_sparkle_1793722651377.jpg"
$baseDir = "C:\Users\munic\Desktop\PreciosPy\mobile\android\app\src\main\res"

$resolutions = @{
    "mipmap-mdpi"    = 48
    "mipmap-hdpi"    = 72
    "mipmap-xhdpi"   = 96
    "mipmap-xxhdpi"  = 144
    "mipmap-xxxhdpi" = 192
}

$srcImage = [System.Drawing.Image]::FromFile($srcPath)

foreach ($folder in $resolutions.Keys) {
    $size = $resolutions[$folder]
    $destPath = Join-Path $baseDir "$folder\ic_launcher.png"
    
    $bmp = New-Object System.Drawing.Bitmap $size, $size
    $graph = [System.Drawing.Graphics]::FromImage($bmp)
    
    $graph.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
    $graph.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::HighQuality
    $graph.PixelOffsetMode = [System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality
    $graph.CompositingQuality = [System.Drawing.Drawing2D.CompositingQuality]::HighQuality

    $graph.DrawImage($srcImage, 0, 0, $size, $size)
    
    if (Test-Path $destPath) {
        Remove-Item $destPath -Force
    }
    
    $bmp.Save($destPath, [System.Drawing.Imaging.ImageFormat]::Png)
    $graph.Dispose()
    $bmp.Dispose()
    
    Write-Output "Generated: $destPath (${size}x${size})"
}

$srcImage.Dispose()
Write-Output "All mipmap icons generated successfully!"

