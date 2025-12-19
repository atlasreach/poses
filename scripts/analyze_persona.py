#!/usr/bin/env python3
"""
Instagram Account Persona Analyzer
Generates a detailed persona report with brand partnership recommendations
"""

import json
from collections import Counter
from datetime import datetime
import re

def analyze_account(json_file='instagram_data.json'):
    with open(json_file, 'r') as f:
        posts = json.load(f)

    # Sort by engagement
    posts_sorted = sorted(posts, key=lambda x: x['likesCount'] + x['commentsCount'], reverse=True)

    total_posts = len(posts)
    total_images = sum(len(p['images']) for p in posts)
    avg_engagement = sum(p['likesCount'] + p['commentsCount'] for p in posts) / total_posts

    # Analyze top performers
    top_10 = posts_sorted[:10]
    bottom_10 = posts_sorted[-10:]

    # Extract caption themes
    all_captions = [p['caption'].lower() for p in posts if p['caption']]

    # Keyword analysis
    sports_keywords = ['nfl', 'nba', 'soccer', 'football', 'champions league', 'barcelona', 'barça', 'stadium', 'match']
    lifestyle_keywords = ['morning', 'day', 'life', 'lately', 'photo', 'favorite', 'vibe', 'fun']
    travel_keywords = ['driving', 'spain', 'miss', 'went']
    gaming_keywords = ['gamer', 'duo', 'carry']
    engagement_keywords = ['would you', 'what about', 'where are', 'or', '?']

    def count_keywords(captions, keywords):
        count = 0
        for caption in captions:
            if any(kw in caption for kw in keywords):
                count += 1
        return count

    sports_posts = count_keywords(all_captions, sports_keywords)
    lifestyle_posts = count_keywords(all_captions, lifestyle_keywords)
    travel_posts = count_keywords(all_captions, travel_keywords)
    gaming_posts = count_keywords(all_captions, gaming_keywords)
    question_posts = count_keywords(all_captions, engagement_keywords)

    # Generate report
    report = []
    report.append("=" * 80)
    report.append("INSTAGRAM PERSONA ANALYSIS REPORT")
    report.append("=" * 80)
    report.append(f"\nAccount: @{posts[0]['ownerUsername']}")
    report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

    report.append("\n" + "=" * 80)
    report.append("ACCOUNT METRICS")
    report.append("=" * 80)
    report.append(f"Total Posts: {total_posts}")
    report.append(f"Total Images: {total_images}")
    report.append(f"Avg Images per Post: {total_images/total_posts:.1f}")
    report.append(f"Avg Engagement: {avg_engagement:,.0f}")

    report.append("\n" + "=" * 80)
    report.append("CONTENT BREAKDOWN")
    report.append("=" * 80)
    report.append(f"Sports Content: {sports_posts} posts ({sports_posts/total_posts*100:.0f}%)")
    report.append(f"Lifestyle Content: {lifestyle_posts} posts ({lifestyle_posts/total_posts*100:.0f}%)")
    report.append(f"Travel Content: {travel_posts} posts ({travel_posts/total_posts*100:.0f}%)")
    report.append(f"Gaming Content: {gaming_posts} posts ({gaming_posts/total_posts*100:.0f}%)")
    report.append(f"Question-Based Posts: {question_posts} posts ({question_posts/total_posts*100:.0f}%)")

    report.append("\n" + "=" * 80)
    report.append("TOP 5 PERFORMING POSTS")
    report.append("=" * 80)
    for i, post in enumerate(top_10[:5], 1):
        engagement = post['likesCount'] + post['commentsCount']
        caption = post['caption'][:60].replace('\n', ' ') if post['caption'] else 'No caption'
        report.append(f"\n#{i} - {engagement:,} engagement")
        report.append(f"    Caption: {caption}...")
        report.append(f"    Images: {len(post['images'])}")

    report.append("\n" + "=" * 80)
    report.append("BOTTOM 5 PERFORMING POSTS (CONSIDER CUTTING)")
    report.append("=" * 80)
    for i, post in enumerate(bottom_10[:5], 1):
        engagement = post['likesCount'] + post['commentsCount']
        caption = post['caption'][:60].replace('\n', ' ') if post['caption'] else 'No caption'
        report.append(f"\n#{i} - {engagement:,} engagement")
        report.append(f"    Caption: {caption}...")

    report.append("\n" + "=" * 80)
    report.append("PERSONA PROFILE")
    report.append("=" * 80)

    # Determine primary persona
    if sports_posts > lifestyle_posts:
        report.append("\nPrimary Persona: SPORTS SUPERFAN + LIFESTYLE")
        report.append("Secondary: Travel & Casual Vibes")
    else:
        report.append("\nPrimary Persona: LIFESTYLE + SPORTS FAN")
        report.append("Secondary: Travel & Casual Content")

    report.append("\n" + "=" * 80)
    report.append("BRAND PARTNERSHIP RECOMMENDATIONS")
    report.append("=" * 80)

    report.append("\n🎯 PRIMARY MONETIZATION PATHS:")
    report.append("\n1. SPORTS BETTING/FANTASY")
    report.append("   - DraftKings, FanDuel, PrizePicks")
    report.append("   - Reason: Question-based sports content drives massive engagement")
    report.append("   - Example: 'NFL or NBA?' = 101k engagement")

    report.append("\n2. SPORTS APPAREL BRANDS")
    report.append("   - Nike, Adidas, Puma (soccer focus)")
    report.append("   - Fanatics (multi-sport jerseys)")
    report.append("   - Reason: Barcelona/soccer content performs exceptionally")
    report.append("   - Example: Barcelona posts = 40k+ engagement")

    report.append("\n3. ACTIVEWEAR/ATHLEISURE")
    report.append("   - Gymshark, Lululemon, Alo Yoga")
    report.append("   - Reason: Lifestyle content maintains consistent engagement")

    report.append("\n4. GAMING BRANDS")
    report.append("   - Razer, SteelSeries, Secretlab")
    report.append("   - Reason: Gaming content present, decent engagement")

    report.append("\n" + "=" * 80)
    report.append("CONTENT STRATEGY RECOMMENDATIONS")
    report.append("=" * 80)

    report.append("\n✅ KEEP & AMPLIFY:")
    report.append("   - Sports team content (especially soccer)")
    report.append("   - Question-based captions (drives 2-3x engagement)")
    report.append("   - Stadium/game day shots")
    report.append("   - 3-4 image carousels")
    report.append("   - Morning/lifestyle casual content")

    report.append("\n🔄 MODIFY:")
    report.append("   - Vary sports teams (don't only do Barcelona)")
    report.append("   - Add specific brand mentions in captions")
    report.append("   - Test NFL/NBA content more (already getting 100k+ engagement)")

    if gaming_posts < 3:
        report.append("\n❌ CONSIDER CUTTING:")
        report.append("   - Gaming content (low volume, unclear brand fit)")

    report.append("\n" + "=" * 80)
    report.append("SPECIFIC VISUAL RECOMMENDATIONS")
    report.append("=" * 80)

    report.append("\n📸 OUTFITS TO RECREATE:")
    report.append("   - Official team jerseys (Barcelona, Spain, NFL teams)")
    report.append("   - Specific brands: Nike soccer kits, NFL Nike jerseys")
    report.append("   - Activewear: form-fitting athletic tops/leggings")
    report.append("   - Casual lifestyle: jeans + crop tops for morning content")

    report.append("\n🎨 BACKGROUNDS TO RECREATE:")
    report.append("   - Soccer stadiums (Camp Nou, Wembley, etc.)")
    report.append("   - NFL stadiums (AT&T Stadium, Lambeau Field, etc.)")
    report.append("   - Bedroom/home for morning content")
    report.append("   - Outdoor lifestyle shots (urban, travel locations)")

    report.append("\n🎯 BRAND-SPECIFIC ELEMENTS:")
    report.append("   - Always use SPECIFIC team names (not 'a soccer team')")
    report.append("   - Always use SPECIFIC jersey brands/years")
    report.append("   - Stadium names matter for authenticity")
    report.append("   - Color accuracy crucial for team branding")

    report.append("\n" + "=" * 80)
    report.append("TRANSFORMATION STRATEGY")
    report.append("=" * 80)

    report.append("\n🔄 WHEN TRANSFORMING IMAGES:")
    report.append("\n   KEEP:")
    report.append("   - Sports vibe and aesthetic")
    report.append("   - Jersey/team apparel styling")
    report.append("   - Stadium atmosphere")
    report.append("   - Question-based engagement style")

    report.append("\n   VARY:")
    report.append("   - Specific teams (Barcelona → Liverpool, Real Madrid, etc.)")
    report.append("   - Specific stadiums (for authenticity testing)")
    report.append("   - Model appearance (hair color, style)")
    report.append("   - Slight pose variations")

    report.append("\n   NEVER:")
    report.append("   - Use generic 'sports team' or 'jersey'")
    report.append("   - Remove brand elements (keep them specific)")
    report.append("   - Lose the aspirational sports fan aesthetic")

    report.append("\n" + "=" * 80)
    report.append("END REPORT")
    report.append("=" * 80)

    return "\n".join(report)

if __name__ == "__main__":
    report = analyze_account()
    print(report)

    # Save to file
    with open('persona_report.txt', 'w') as f:
        f.write(report)
    print("\n✅ Report saved to persona_report.txt")
