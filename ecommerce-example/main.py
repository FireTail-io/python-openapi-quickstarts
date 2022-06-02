#!/usr/bin/env python3
import json
from random import randint
from randomuser import RandomUser
import pointsecio
import datetime
import logging

from pointsecio import NoContent
from pointsecio.auditor import request_auditor

# our memory-only pet storage
from pointsecio.exceptions import OAuthProblem
from requests import get

from pointsecio import request

TOKEN_DB = {
    'asdf1234567890': {
        'uid': 100
    }
}


def apikey_auth(token, required_scopes):
    info = TOKEN_DB.get(token, None)

    if not info:
        raise OAuthProblem('Invalid token')

    return info


PRODUCTS = {
    "1": {
        "product_id": 1,
        "product_name": "Fjallraven - Foldsack No. 1 Backpack, Fits 15 Laptops",
        "product_price": 109.95,
        "product_description": "Your perfect pack for everyday use and walks in the forest. Stash your laptop (up to 15 inches) in the padded sleeve, your everyday",
        "product_type": "clothing",
        "product_status": "available",
        "product_rating": {
            "rate": 3.9,
            "count": 120
        }
    },
    "2": {
        "product_id": 2,
        "product_name": "Mens Casual Premium Slim Fit T-Shirts ",
        "product_price": 22.3,
        "product_description": "Slim-fitting style, contrast raglan long sleeve, three-button henley placket, light weight & soft fabric for breathable and comfortable wearing. And Solid stitched shirts with round neck made for durability and a great fit for casual fashion wear and diehard baseball fans. The Henley style round neckline includes a three-button placket.",
        "product_type": "clothing",
        "product_status": "available",
        "product_rating": {
            "rate": 4.1,
            "count": 259
        }
    },
    "3": {
        "product_id": 3,
        "product_name": "Mens Cotton Jacket",
        "product_price": 55.99,
        "product_description": "great outerwear jackets for Spring/Autumn/Winter, suitable for many occasions, such as working, hiking, camping, mountain/rock climbing, cycling, traveling or other outdoors. Good gift choice for you or your family member. A warm hearted love to Father, husband or son in this thanksgiving or Christmas Day.",
        "product_type": "clothing",
        "product_status": "available",
        "product_rating": {
            "rate": 4.7,
            "count": 500
        }
    },
    "4": {
        "product_id": 4,
        "product_name": "Mens Casual Slim Fit",
        "product_price": 15.99,
        "product_description": "The color could be slightly different between on the screen and in practice. / Please note that body builds vary by person, therefore, detailed size information should be reviewed below on the product product_description.",
        "product_type": "clothing",
        "product_status": "available",
        "product_rating": {
            "rate": 2.1,
            "count": 430
        }
    },
    "5": {
        "product_id": 5,
        "product_name": "John Hardy Women's Legends Naga Gold & Silver Dragon Station Chain Bracelet",
        "product_price": 695,
        "product_description": "From our Legends Collection, the Naga was inspired by the mythical water dragon that protects the ocean's pearl. Wear facing inward to be bestowed with love and abundance, or outward for protection.",
        "product_type": "jewelery",
        "product_status": "soldout",
        "product_rating": {
            "rate": 4.6,
            "count": 400
        }
    },
    "6": {
        "product_id": 6,
        "product_name": "Solid Gold Petite Micropave ",
        "product_price": 168,
        "product_description": "Satisfaction Guaranteed. Return or exchange any order within 30 days.Designed and sold by Hafeez Center in the United States. Satisfaction Guaranteed. Return or exchange any order within 30 days.",
        "product_type": "jewelery",
        "product_status": "available",
        "product_rating": {
            "rate": 3.9,
            "count": 70
        }
    },
    "7": {
        "product_id": 7,
        "product_name": "White Gold Plated Princess",
        "product_price": 9.99,
        "product_description": "Classic Created Wedding Engagement Solitaire Diamond Promise Ring for Her. Gifts to spoil your love more for Engagement, Wedding, Anniversary, Valentine's Day...",
        "product_type": "jewelery",
        "product_status": "available",
        "product_rating": {
            "rate": 3,
            "count": 400
        }
    },
    "8": {
        "product_id": 8,
        "product_name": "Pierced Owl Rose Gold Plated Stainless Steel Double",
        "product_price": 10.99,
        "product_description": "Rose Gold Plated Double Flared Tunnel Plug Earrings. Made of 316L Stainless Steel",
        "product_type": "jewelery",
        "product_status": "available",
        "product_rating": {
            "rate": 1.9,
            "count": 100
        }
    },
    "9": {
        "product_id": 9,
        "product_name": "WD 2TB Elements Portable External Hard Drive - USB 3.0 ",
        "product_price": 64,
        "product_description": "USB 3.0 and USB 2.0 Compatibility Fast data transfers Improve PC Performance High Capacity; Compatibility Formatted NTFS for Windows 10, Windows 8.1, Windows 7; Reformatting may be required for other operating systems; Compatibility may vary depending on user’s hardware configuration and operating system",
        "product_type": "electronics",
        "product_status": "available",
        "product_rating": {
            "rate": 3.3,
            "count": 203
        }
    },
    "10": {
        "product_id": 10,
        "product_name": "SanDisk SSD PLUS 1TB Internal SSD - SATA III 6 Gb/s",
        "product_price": 109,
        "product_description": "Easy upgrade for faster boot up, shutdown, application load and response (As compared to 5400 RPM SATA 2.5” hard drive; Based on published specifications and internal benchmarking tests using PCMark vantage scores) Boosts burst write performance, making it ideal for typical PC workloads The perfect balance of performance and reliability Read/write speeds of up to 535MB/s/450MB/s (Based on internal testing; Performance may vary depending upon drive capacity, host device, OS and application.)",
        "product_type": "electronics",
        "product_status": "soldout",
        "product_rating": {
            "rate": 2.9,
            "count": 470
        }
    },
    "11": {
        "product_id": 11,
        "product_name": "Silicon Power 256GB SSD 3D NAND A55 SLC Cache Performance Boost SATA III 2.5",
        "product_price": 109,
        "product_description": "3D NAND flash are applied to deliver high transfer speeds Remarkable transfer speeds that enable faster bootup and improved overall system performance. The advanced SLC Cache Technology allows performance boost and longer lifespan 7mm slim design suitable for Ultrabooks and Ultra-slim notebooks. Supports TRIM command, Garbage Collection technology, RAID, and ECC (Error Checking & Correction) to provide the optimized performance and enhanced reliability.",
        "product_type": "electronics",
        "product_status": "available",
        "product_rating": {
            "rate": 4.8,
            "count": 319
        }
    },
    "12": {
        "product_id": 12,
        "product_name": "WD 4TB Gaming Drive Works with Playstation 4 Portable External Hard Drive",
        "product_price": 114,
        "product_description": "Expand your PS4 gaming experience, Play anywhere Fast and easy, setup Sleek design with high capacity, 3-year manufacturer's limited warranty",
        "product_type": "electronics",
        "product_status": "available",
        "product_rating": {
            "rate": 4.8,
            "count": 400
        }
    },
    "13": {
        "product_id": 13,
        "product_name": "Acer SB220Q bi 21.5 inches Full HD (1920 x 1080) IPS Ultra-Thin",
        "product_price": 599,
        "product_description": "21. 5 inches Full HD (1920 x 1080) widescreen IPS display And Radeon free Sync technology. No compatibility for VESA Mount Refresh Rate: 75Hz - Using HDMI port Zero-frame design | ultra-thin | 4ms response time | IPS panel Aspect ratio - 16: 9. Color Supported - 16. 7 million colors. Brightness - 250 nit Tilt angle -5 degree to 15 degree. Horizontal viewing angle-178 degree. Vertical viewing angle-178 degree 75 hertz",
        "product_type": "electronics",
        "product_status": "available",
        "product_rating": {
            "rate": 2.9,
            "count": 250
        }
    },
    "14": {
        "product_id": 14,
        "product_name": "Samsung 49-Inch CHG90 144Hz Curved Gaming Monitor (LC49HG90DMNXZA) Super Ultrawide Screen QLED ",
        "product_price": 999.99,
        "product_description": "49 INCH SUPER ULTRAWIDE 32:9 CURVED GAMING MONITOR with dual 27 inch screen side by side QUANTUM DOT (QLED) TECHNOLOGY, HDR support and factory calibration provides stunningly realistic and accurate color and contrast 144HZ HIGH REFRESH RATE and 1ms ultra fast response time work to eliminate motion blur, ghosting, and reduce input lag",
        "product_type": "electronics",
        "product_status": "available",
        "product_rating": {
            "rate": 2.2,
            "count": 140
        }
    },
    "15": {
        "product_id": 15,
        "product_name": "BIYLACLESEN Women's 3-in-1 Snowboard Jacket Winter Coats",
        "product_price": 56.99,
        "product_description": "Note:The Jackets is US standard size, Please choose size as your usual wear Material: 100% Polyester; Detachable Liner Fabric: Warm Fleece. Detachable Functional Liner: Skin Friendly, Lightweigt and Warm.Stand Collar Liner jacket, keep you warm in cold weather. Zippered Pockets: 2 Zippered Hand Pockets, 2 Zippered Pockets on Chest (enough to keep cards or keys)and 1 Hidden Pocket Inside.Zippered Hand Pockets and Hidden Pocket keep your things secure. Humanized Design: Adjustable and Detachable Hood and Adjustable cuff to prevent the wind and water,for a comfortable fit. 3 in 1 Detachable Design provide more convenience, you can separate the coat and inner as needed, or wear it together. It is suitable for different season and help you adapt to different climates",
        "product_type": "clothing",
        "product_status": "soldout",
        "product_rating": {
            "rate": 2.6,
            "count": 235
        }
    },
    "16": {
        "product_id": 16,
        "product_name": "Lock and Love Women's Removable Hooded Faux Leather Moto Biker Jacket",
        "product_price": 29.95,
        "product_description": "100% POLYURETHANE(shell) 100% POLYESTER(lining) 75% POLYESTER 25% COTTON (SWEATER), Faux leather material for style and comfort / 2 pockets of front, 2-For-One Hooded denim style faux leather jacket, Button detail on waist / Detail stitching at sides, HAND WASH ONLY / DO NOT BLEACH / LINE DRY / DO NOT IRON",
        "product_type": "clothing",
        "product_status": "available",
        "product_rating": {
            "rate": 2.9,
            "count": 340
        }
    }
}




def health():
    return {'status': 'UP'}

def get_products(limit, product_type=None):
    print("product_type: ", product_type)
    return {"products": [product for product in PRODUCTS.values() if not product_type or product['product_type'] == product_type][:limit]}

def get_available_products():
    return {"products": [product for product in PRODUCTS.values() if product['product_status'] == "available"]}

def get_product(product_id):
    product = PRODUCTS.get(product_id)
    return product or ("Not found", 404)

def put_product(product_id):
    product = request.json
    exists = str(product_id) in PRODUCTS
    product['product_id'] = product_id
    if exists:
        print("Found product ", product_id)
        try:
            PRODUCTS[product_id].update(product)
        except:
            print("An exception occured while trying to update product")
    else:
        print("Did not Find product..will try to create a new product ", product_id)
        product['created'] = datetime.datetime.utcnow()
        try:
            PRODUCTS[product_id] = product
        except:
            print("An exception occured while trying to create a product")
    return NoContent, (200 if exists else 201)

def delete_product(product_id):
    if str(product_id) in PRODUCTS:
        print("Found product ", product_id)
        try:
            del PRODUCTS[str(product_id)]
        except:
            print("Exception occured during deletion of product")
        return NoContent, 204
    else:
        return NoContent, 404

def get_product_availability(product_id):
    exists = str(product_id) in PRODUCTS
    if exists:
        counter = randint(1,10)
        if(counter > 5):
            message = "product " + product_id + " is available"
        else:
            message = "product " + product_id + " is not available"
        return json.dumps({"message": message}), 200
    else:
        return NoContent, 404

def put_cart():
    counter = randint(1,10)
    if(counter > 5):
        message = "Item has been added successfully"
    else:
        message = "Failed to add to cart"
    return json.dumps({"message": message}), 200

def get_checkout():
    counter = randint(1,10)
    if(counter > 5):
        message = "Checkout success"
    else:
        message = "Checkout failed"
    return json.dumps({"message": message}), 200

def get_profile():
    user = RandomUser({'nat': 'ca'})
    return {
        "first_name": user.get_first_name(),
        "last_name": user.get_last_name(),
        "username": user.get_username(),
        "dob": datetime.datetime.strptime(user.get_dob(),'%Y-%m-%dT%H:%M:%S.%fZ').date(),
        "state": user.get_state(),
        "postcode": user.get_postcode()
        }



logging.basicConfig(level=logging.INFO)
app = pointsecio.App(__name__)

app.add_api('ecommerce-example.yaml')



if __name__ == '__main__':
    app.debug = True
    app.run(port=8080, threaded=True)
