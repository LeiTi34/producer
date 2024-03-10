#!/bin/env sh

export KAFKA_BROKER_URL="localhost:29092"
export KAFKA_TOPIC="products"
export SCHEMA_REGISTRY_URL="http://localhost:8081"

export API_CONFIGS='[
  {
      "url": "https://www.penny.at/api/categories/bier-und-radler-13026/products?page={PAGE}&pageSize={PAGE_SIZE}",
      "name": "penny",
      "page_size": 100
  },
  {
      "url": "https://shop.billa.at/api/categories/bier-und-radler-13796/products?page={PAGE}&pageSize={PAGE_SIZE}&storeId=00-10",
      "name": "billa",
      "page_size": 100
  }
]'
