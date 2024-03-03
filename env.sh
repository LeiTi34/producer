#!/bin/env sh

export KAFKA_BROKER_URL="localhost:29092"

export API_CONFIGS='[
  {
      "URL": "https://www.penny.at/api/categories/angebote-ab-2202/products?page={PAGE}&pageSize={PAGE_SIZE}",
      "TOPIC": "penny"
  },
  {
      "URL": "https://shop.billa.at/api/categories/getraenke-13784/products?page={PAGE}&pageSize={PAGE_SIZE}&storeId=00-10",
      "TOPIC": "billa"
  }
]'
