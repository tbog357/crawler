<!-- Requirements: 
viet 1 chuong trinh bằng PHP chay tren may local de cu 10 phut
đọc ra tất cả các sản phẩm từ trang https://shopee.vn/shop/16461019/search
lưu tất cả các sản phẩm xuống MySql DB

cụ thể hệ thống cần có những components sau:

# 1. scheduler viết bằng crontab -> trigger 1 hàm viết bằng php để tạo ra 1 job có format như sau:
{
    "url": "https://shopee.vn/shop/16461019/search",
    "interval": 600
}

gửi job vào queue dưới
# 2. queue dùng dev rabbitmq:  http://192.168.4.201:15672/#/queues  
dmx_test / dmx_test  (
    tạo 1 exchange mới
    http://192.168.4.201:15672/#/exchanges/%2F/dmx_test_exchange
    , 
    mỗi bạn dùng 1 queue
    http://192.168.4.201:15672/#/queues/%2F/anker_1
    http://192.168.4.201:15672/#/queues/%2F/anker_2
) 

# 3. 1 scraper viết bằng PHP luôn luôn chạy background (dùng tmux) lấy job message từ queue ra format thành json có dạng dưới

# 4. sau khi có thông tin sản phẩm có dạng:
{
    "name": "",
    "url": "",
    "rrp_price": 0,
    "sale_price": 0,
    "stock" : 0
}

luu xuong 1 table trên mysql với những field tương ứng, dùng auto increment ID 
DB DEV đã cấp quyền, DB tên: test. (tạo table mới cho mỗi bạn)

- dựng 1 backend service viết bằng golang chỉ làm nhiệm vụ downloading, yêu cầu dùng goroutine để chạy multi threading equivalent (x10 threads)
- sửa hàm hiện tại đang dùng php để download -> đẩy job qua 1 queue (đặt tên là download_jobs) -> golang backend service bên trên nhận job, download -> gửi lại kết quả vào 1 queue khác download_results -> php nhận -> insert xuống DB
- không chỉ lấy list sản phẩm như hiện tại mà cần lấy details của từng sản phẩm & lưu xuống DB (cần gọi thêm 1 call để get details cho mỗi sản phẩm cấu trúc table products_details tự dựng nhé)

prerequisites:
using goland IDE
golang 
goroutine
build & compile go

# Products Table 
id, name, url, shop_id, categoy_id, description, 

sudo lsof -n -i | grep 5672

# Structure
(10th min send job from crontab) -> download_jobs (php) -> rabbitmq (download_jobs) -> downloader (golang) -> rabbitmq (download_results)-> data_inserter (php) 

id
name
url
deep_discount
normal_stock
price_min_before_discount
price_max_before_discount
discount_stock
description
models 

Services"
mysql
rabbitmq
elasticsearch
kibana

go 
php
-->


<!-- # List shop id 
https://shopee.vn/shop/185522883/search
https://shopee.vn/shop/191065034/search
https://shopee.vn/shop/16461019/search -->

# Env
Mysql (localhost)

RabbitMQ (localhost)

# Commands
### Run rabbitmq container 
sudo docker run -d -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management

### Create queue, exchange and table in mysql
php create_pipelines.php

### Create a pane with tmux
tmux new-session -t anker

### TMUX: Run downloader in anker pane
go ./downloader/downloader

### TMUX: Run downloader in another window in anker pane
php results_consumer.php 

### Start download_jobs
php download_jobs.php

### Setup crontab for download jobs
*/10 * * * * php /path/to/download_jobs.php

## Run container 

sudo docker run -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.10.2

sudo docker run -d --link 3f63918e7237:elasticsearch -p 5601:5601 docker.elastic.co/kibana/kibana:7.10.2


# Structure
download_jobs (php) -> queue (DOWNLOAD_JOBS) -> downloader (golang) -> queue(DOWNLOAD_RESULTS) -> results_consumer (php)
                                                rpc call 
<!-- 
1. Read same configuration from file
2. Handle network status -->