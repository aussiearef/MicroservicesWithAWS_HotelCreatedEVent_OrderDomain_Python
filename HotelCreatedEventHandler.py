import json
import boto3
from boto3.dynamodb.conditions import Key
from datetime import datetime
from typing import Optional

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Hotels_Order_Domain')

class Hotel:
    def __init__(self, user_id: Optional[str] = None, hotel_id: Optional[str] = None, 
                 name: Optional[str] = None, city_name: Optional[str] = None, 
                 price: Optional[int] = None, rating: Optional[int] = None, 
                 creation_date_time: Optional[datetime] = None, 
                 file_name: Optional[str] = None):
        self.UserId = user_id
        self.Id = hotel_id
        self.Name = name
        self.CityName = city_name
        self.Price = price
        self.Rating = rating
        self.CreationDateTime = creation_date_time
        self.FileName = file_name

    @classmethod
    def from_json(cls, json_str: str):
        json_dict = json.loads(json_str)
        return cls(**json_dict)

    def to_dict(self):
        return {
            'userId': self.UserId,
            'Id': self.Id,
            'Name': self.Name,
            'CityName': self.CityName,
            'Price': self.Price,
            'Rating': self.Rating,
            'CreationDateTime': self.CreationDateTime.isoformat(),
            'FileName': self.FileName,
        }

def handler(event, context):
    for record in event['Records']:
        hotel = Hotel.from_json(record['Sns']['Message'])
        table.put_item(Item=hotel.to_dict())
