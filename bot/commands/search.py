import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import random


class RestaurantView(discord.ui.View):
    """餐厅分页的视图（包含按钮）"""
    
    def __init__(self, restaurants: list, current_page: int = 0):
        super().__init__(timeout=300)  # 5 分钟超时
        self.restaurants = restaurants
        self.current_page = current_page
        self.total_pages = len(restaurants)
        
        # 根据当前页码决定按钮是否可用
        self.update_buttons()
    
    def update_buttons(self):
        """更新按钮的可用状态"""
        # 找到按钮
        prev_button = None
        next_button = None
        
        for item in self.children:
            if isinstance(item, discord.ui.Button):
                if item.label == "⬅️":
                    prev_button = item
                elif item.label == "➡️":
                    next_button = item
        
        # 如果在第一页，左箭头禁用
        if prev_button:
            prev_button.disabled = (self.current_page == 0)
        
        # 如果在最后一页，右箭头禁用
        if next_button:
            next_button.disabled = (self.current_page >= self.total_pages - 1)
    
    @discord.ui.button(label="⬅️", style=discord.ButtonStyle.primary)
    async def prev_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        """上一页"""
        if self.current_page > 0:
            self.current_page -= 1
            
            # 获取新的餐厅数据
            restaurant = self.restaurants[self.current_page]
            
            # 构建新的 Embed
            embed = self._build_embed(restaurant, self.current_page)
            
            # 创建新的 View（重新生成按钮）
            new_view = RestaurantView(self.restaurants, self.current_page)
            
            # 编辑消息
            await interaction.response.edit_message(embed=embed, view=new_view)
    
    @discord.ui.button(label="➡️", style=discord.ButtonStyle.primary)
    async def next_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        """下一页"""
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            
            # 获取新的餐厅数据
            restaurant = self.restaurants[self.current_page]
            
            # 构建新的 Embed
            embed = self._build_embed(restaurant, self.current_page)
            
            # 创建新的 View（重新生成按钮）
            new_view = RestaurantView(self.restaurants, self.current_page)
            
            # 编辑消息
            await interaction.response.edit_message(embed=embed, view=new_view)
    
    @staticmethod
    def _build_embed(restaurant: dict, page_number: int) -> discord.Embed:
        """构建 Embed 卡片"""
        embed = discord.Embed(
            title=f"🍽️ {restaurant['name']}",
            description=f"⭐ {restaurant['rating']:.1f}/5.0 | 📍 {restaurant['location']}",
            url=restaurant['url'],
            color=discord.Color.gold()
        )
        embed.add_field(
            name="Average Price",
            value=f"${restaurant['price']:.2f}",
            inline=True
        )
        embed.add_field(
            name="Review Count",
            value=f"{restaurant['review_count']} reviews",
            inline=True
        )
        embed.set_footer(text=f"Page {page_number + 1}")  # 显示页码（从 1 开始）
        return embed


class SearchCog(commands.Cog):
    """搜索餐厅的 Cog"""
    
    def __init__(self, bot):
        self.bot = bot
        
        # 湾区城市和对应的价格（人均消费，美元）
        self.city_price_map = {
            "San Francisco": 35.0,
            "Oakland": 15.0,
            "San Jose": 18.0,
            "Berkeley": 20.0,
            "Palo Alto": 40.0,
            "Mountain View": 25.0,
            "Sunnyvale": 22.0,
            "Fremont": 16.0,
            "Hayward": 14.0,
            "Daly City": 12.0,
            "Walnut Creek": 24.0,
            "Pleasanton": 23.0,
            "Livermore": 19.0,
            "Concord": 17.0,
            "Vallejo": 13.0,
            "Richmond": 11.0,
            "Redwood City": 28.0,
            "Menlo Park": 38.0,
            "Cupertino": 32.0,
            "Santa Clara": 20.0
        }
    
    def generate_mock_restaurants(self, cuisine: str, area: str, count: int = 20) -> list:
        """
        生成 Mock 餐厅列表
        
        Args:
            cuisine: 菜系（如 "sushi", "burger"）
            area: 地区（如 "sf", "sj"）
            count: 生成的餐厅数量
        
        Returns:
            包含 count 个餐厅字典的列表
        """
        restaurants = []
        cities = list(self.city_price_map.keys())
        
        for i in range(count):
            # 轮流选择城市（确保不重复）
            city = cities[i % len(cities)]
            price = self.city_price_map[city]
            
            restaurant = {
                "name": f"{cuisine.capitalize()} Restaurant #{i + 1}",
                "rating": round(random.uniform(1.5, 5.0), 1),  # 随机评分 1.5-5.0
                "review_count": random.randint(10, 500),  # 随机评价数
                "location": f"{(i + 1) * 100} Main St, {city}",  # 不同的地址
                "price": price,  # 根据城市的固定价格
                "url": "https://www.yelp.com"
            }
            restaurants.append(restaurant)
        
        return restaurants
    
    @app_commands.command(name="find_food", description="在湾区寻找美食")
    @app_commands.describe(
        cuisine="想吃什么菜系？(如: sushi, burger, ramen)",
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
        """搜索餐厅命令"""
        # 立即响应，防止 Discord 3 秒超时
        await interaction.response.defer()
        
        # 模拟网络请求延迟
        await asyncio.sleep(1.5)
        
        # 生成 20 个 Mock 餐厅
        restaurants = self.generate_mock_restaurants(cuisine, area, count=20)
        
        # 获取第一家餐厅
        first_restaurant = restaurants[0]
        
        # 构建 Embed 卡片
        embed = RestaurantView._build_embed(first_restaurant, page_number=0)
        
        # 创建分页 View
        view = RestaurantView(restaurants, current_page=0)
        
        # 发送消息
        await interaction.followup.send(
            content="✅ 找到 20 家不错的餐厅！使用按钮翻页。",
            embed=embed,
            view=view
        )


# 标准的 Cog 注册函数
async def setup(bot):
    await bot.add_cog(SearchCog(bot))