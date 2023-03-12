<?php

// Local import 
include "parser/utils.php";

// Client for sending jobs to downloader 
$jobSender = new RabbitMQ();

// Input 
$shopIds = ["191065034", "185522883", "16461019"];

foreach ($shopIds as $shopId) {
    echo $shopId ."\n";
    // Generate job
    $job = [
        "platform" => "shopee",
        "shopId" => $shopId,
        "jobType" => "itemsList", // or item
        "url" => "https://shopee.vn/api/v2/search_items/?by=pop&limit=30&match_id=" . $shopId . "&newest=0&order=desc&page_type=shop&version=2", 
        "page" => 0
    ];

    // Send job to downloader 
    $jobSender->produce(json_encode($job), EXCHANGE_NAME, KEY_JOBS);
}
