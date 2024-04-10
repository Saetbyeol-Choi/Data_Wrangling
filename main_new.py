# from fastapi import FastAPI
# import json
# import requests
# from bs4 import BeautifulSoup
#
# app = FastAPI()
#
# with open("C:/Users/sbyeo/Downloads/tablets.json/tablets.json", "r") as f:
#     data = json.load(f)
#
# # Add an 'id' field to each dictionary in the 'tablets' list
# for i, tablet in enumerate(data):
#     tablet["id"] = i
#
# #print(data)
#
# @app.get("/")
# async def root():
#     return {"What is the Best Tablet for Students Overall?"}
#
# # Endpoint to get all tablets
# @app.get("/tablets")
# async def get_all_tablets():
#     return data
#
# # Endpoint to get brand name of tablets
# @app.get("/tablets/brands")
# async def get_tablets():
#     unique_brands = set(d["Brand"] for d in data)
#     sorted_brands = sorted(unique_brands)
#     return sorted_brands
#
# # Endpoint to get a specific tablet by ID
# @app.get("/tablets/{tablet_id}")
# async def get_tablet_by_id(tablet_id: int):
#     for tablet in data:
#         if tablet["id"] == tablet_id:
#             return tablet
#     return {"error": "Tablet not found"}
#
# # Endpoint to search for tablets by brand
# @app.get("/tablets/search/{brand}")
# async def search_tablets_by_brand(brand: str):
#     results = []
#     for tablet in data:
#         if tablet["Brand"].lower() == brand.lower():
#             results.append(tablet)
#     if results:
#         return results
#     return {"error": "No tablets found with that brand"}
#
# # Endpoint to get the average rating for a specific tablet by ID
# @app.get("/tablets/{tablet_id}/rating")
# async def get_average_rating(tablet_id: int):
#     for tablet in data:
#         if tablet["id"] == tablet_id:
#             try:
#                 ratings = [int(tablet["5 Stars"]), int(tablet["4 Stars"]), int(tablet["3 Stars"]), int(tablet["2 Stars"]), int(tablet["1 Stars"])]
#                 total_ratings = sum(ratings)
#                 if total_ratings == 0:
#                     return {"average_rating": "No ratings yet"}
#                 weighted_ratings = [5*int(tablet["5 Stars"]), 4*int(tablet["4 Stars"]), 3*int(tablet["3 Stars"]), 2*int(tablet["2 Stars"]), 1*int(tablet["1 Stars"])]
#                 average_rating = round(sum(weighted_ratings) / total_ratings,1)
#                 return {"average_rating": average_rating}
#             except (ValueError, KeyError):
#                 return {"error": "Invalid or missing rating data"}
#     return {"error": "Tablet not found"}
#
# # Endpoint to get the top 10 tablets by rating         # still working on
# # @app.get("/tablets/top-rated")
# # async def get_top_rated_tablets():
# #     # Calculate the average rating for each tablet
# #     for tablet in data:
# #         ratings = [int(tablet["5 Stars"]), int(tablet["4 Stars"]), int(tablet["3 Stars"]), int(tablet["2 Stars"]), int(tablet["1 Stars"])]
# #         total_ratings = sum(ratings)
# #         if total_ratings == 0:
# #             tablet["average_rating"] = None
# #         else:
# #             weighted_ratings = [5*int(tablet["5 Stars"]), 4*int(tablet["4 Stars"]), 3*int(tablet["3 Stars"]), 2*int(tablet["2 Stars"]), 1*int(tablet["1 Stars"])]
# #             average_rating = round(sum(weighted_ratings) / total_ratings,1)
# #             tablet["average_rating"] = average_rating
# #
# #     # Sort the tablets by their average rating
# #     sorted_data = sorted(data, key=lambda tablet: tablet["average_rating"], reverse=True)
# #
# #     # Return the top 10 tablets
# #     return sorted_data[:10]
#
#
# # Endpoint to get the top 10+ best tablets for Students in 2023 from the website
# # url = "https://justcreative.com/best-tablets-for-students/"
# # response = requests.get(url)
# #
# # if response.status_code == 200:
# #     soup = BeautifulSoup(response.content, "html.parser")
# #
# #     # find all the tablet names
# #     names = []
# #     for tablet in soup.select("ol > li > a"):
# #         name = tablet.text.strip()
# #         if name.startswith(("1.", "2.", "3.", "4.", "5.", "6.", "7.", "8.", "9.", "10.", "11.", "12.", "13.")):
# #             names.append(name)
# #
# #     # do something with the tablet names
# #     print(names)
# #
# # else:
# #     print(f"Error: {response.status_code}")
#
# # # create the endpoint
# # @app.get("/best_tablets")
# # async def get_best_tablet_names():
# #     return {"10+ Best Tablets for Students in 2023": names}
#
# import re
#
# url = "https://justcreative.com/best-tablets-for-students/"
# response = requests.get(url)
#
# if response.status_code == 200:
#     soup = BeautifulSoup(response.content, "html.parser")
#
#     # find all the tablet names
#     names = []
#     for tablet in soup.select("ol > li > a"):
#         name = tablet.text.strip()
#         if re.match(r"^\d+\.", name):
#             names.append(name)
#
#     # sort the tablet names by their number
#     names.sort(key=lambda x: int(x.split(".")[0]))
#
#     # do something with the tablet names
#     tablets = "<br>".join(names)
#     best_t = {"10+ Best Tablets for Students in 2023": tablets}
#
# else:
#     print(f"Error: {response.status_code}")
#
# @app.get("/best_tablets")
# async def get_best_tablet_names():
#     response = best_t.copy()
#     tablets = response["10+ Best Tablets for Students in 2023"]
#     tablets = tablets.split("\n")
#     tablets = "<br>".join(tablets)
#     response["10+ Best Tablets for Students in 2023"] = tablets
#     return response
