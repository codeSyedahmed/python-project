<?php

// List of URLs to scrape
$urls = [
    "https://www.ashford.com/brand/glycine.html"
];

// Markup multiplier
$markupMultiplier = 1.2;  // You can adjust this value as needed

// Preloaded list of SKUs
$preloadedSkus = ["123", "456", "789"];  // Add your SKUs here

// Output file name
$outputFile = "output.csv";

function calculateMarkedUpPrice($price)
{
    global $markupMultiplier;
    return ($price * $markupMultiplier) + 10;
}

function scrapeData($url)
{
    $response = file_get_contents($url);

    if ($response !== false) {
        $dom = new DOMDocument;
        libxml_use_internal_errors(true);
        $dom->loadHTML($response);
        libxml_clear_errors();

        $xpath = new DOMXPath($dom);

        $skuElements = $xpath->query('//*[@data-product-sku]');
        $priceElements = $xpath->query('//span[@class="price"]');

        $scrapedData = [];

        foreach ($skuElements as $index => $skuElement) {
            $sku = $skuElement->getAttribute('data-product-sku');
            $priceText = $priceElements[$index]->textContent;
            $price = floatval(str_replace(['$', ','], '', $priceText));
            $markedUpPrice = calculateMarkedUpPrice($price);
            $scrapedData[] = [$sku, $markedUpPrice, 1];
        }

        return $scrapedData;
    }

    return [];
}

function main()
{
    global $urls, $outputFile, $preloadedSkus;

    $allData = [];

    foreach ($urls as $url) {
        $data = scrapeData($url);
        $allData = array_merge($allData, $data);
    }

    // Write data to output file
    $output = fopen($outputFile, 'w');
    fwrite($output, "SKU,PRICE,QUANTITY\n");

    foreach ($allData as [$sku, $markedUpPrice, $quantity]) {
        fwrite($output, "$sku,$markedUpPrice,$quantity\n");
    }

    // Add SKUs not scraped
    foreach ($preloadedSkus as $sku) {
        if (!in_array($sku, array_column($allData, 0))) {
            fwrite($output, "$sku,100.00,0\n");  // Assign a random price (e.g., 100) and quantity 0
        }
    }

    fclose($output);
}

main();
echo "Conversion completed successfully.\n";
?>
