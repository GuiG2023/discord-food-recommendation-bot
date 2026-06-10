import discord
from discord.ext import commands
from discord import app_commands
import asyncio

class SearchCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="find_food", description="在湾区寻找美食")
    @app_commands.describe(
        cuisine="想吃什么菜系？(如: sushi, burger)",
        area="哪个区域？(如: sf, sj, oakland)",
        budget="价位预期 ($, $$, $$$, $$$$)"
    )
    async def find_food(
        self, 
        interaction: discord.Interaction, 
        cuisine: str, 
        area: str = "sf", 
        budget: str = "$$"
    ):
        await interaction.response.defer()
        await asyncio.sleep(1.5)

        mock_restaurant = {
            "name": f"Fake {cuisine.capitalize()} Place",
            "rating": 4.8,
            "review_count": 312,
            "location": f"123 Mockingbird Ln, {area.upper()}",
            "price": budget,
            "url": "https://www.yelp.com"
        }

        embed = discord.Embed(
            title=f"🍽️ {mock_restaurant['name']}",
            description=f"⭐ {mock_restaurant['rating']}/5.0 | 📍 {mock_restaurant['location']}",
            url=mock_restaurant['url'],
            color=discord.Color.gold()
        )
        embed.add_field(name="价位", value=mock_restaurant['price'], inline=True)
        embed.add_field(name="评价数", value=f"{mock_restaurant['review_count']} 条", inline=True)

        await interaction.followup.send(content="✅ 找到一家不错的餐厅！", embed=embed)

async def setup(bot):
    await bot.add_cog(SearchCog(bot))