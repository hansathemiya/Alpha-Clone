import requests
import argparse
import getpass
import subprocess
from bs4 import BeautifulSoup

def display_startup_message():
    ascii_art = """
    AAAA     LLL      PPPPP    HHH   HHH    AAAA     CCCCCC   LLL        OOOOO    NNN    NNN  EEEEEEEE
   AAAAA    LLL      PPPPPPP   HHH   HHH   AAAAAA   CCCCCCCC  LLL       OOOOOOO   NNNN   NNN  EEEEEEEE
  AAA AAA   LLL      PPP  PPP  HHH   HHH  AAA  AAA CCC        LLL      OOO   OOO  NNNNN  NNN  EEE     
 AAA   AAA  LLL      PPPPPPP   HHHHHHHHH AAAA  AAA CCC        LLL      OOO   OOO  NNNNNN NNN  EEEEE  
 AAAAAAAAAA LLL      PPPPP     HHHHHHHHH AAAAAAAAA CCC        LLL      OOO   OOO  NNN NNNNNN  EEEEE  
 AAA     AAA LLL      PPP       HHH   HHH AAA    AA CCC        LLL      OOO   OOO  NNN  NNNNN  EEE     
 AAA     AAA LLLLLLLL PPP       HHH   HHH AAA    AAA CCCCCCCC  LLLLLLLL  OOOOOOO   NNN   NNNN  EEEEEEEE
 AAA     AAA LLLLLLLL PPP       HHH   HHH AAA    AAA   CCCCCC   LLLLLLL    OOOOO    NNN    NNN  EEEEEEEE

                                  By Hansa Themiya
    """
    print(ascii_art)

def fetch_profile_data(url, platform):
    try:
        if platform == '1':
            # Using curl to fetch profile data
            profile_username = url.split('/')[-1]
            subprocess.run(['curl', '-L', f'https://www.instagram.com/{profile_username}/', '-o', 'profile.html'])
            
            with open('profile.html', 'r', encoding='utf-8') as file:
                html_content = file.read()
            
            soup = BeautifulSoup(html_content, 'html.parser')
            
            profile_data = {
                'profile_pic_url': soup.find('meta', property='og:image')['content'],
                'posts': [],
                'following': [],
                'followers': []
            }
            
            for script in soup.find_all('script', type='text/javascript'):
                if 'window._sharedData = ' in script.string:
                    shared_data = script.string.split('window._sharedData = ')[1].rstrip(';')
                    shared_data = json.loads(shared_data)
                    user_data = shared_data['entry_data']['ProfilePage'][0]['graphql']['user']
                    
                    profile_data['following'] = [edge['node']['username'] for edge in user_data['edge_follow']['edges']]
                    profile_data['followers'] = [edge['node']['username'] for edge in user_data['edge_followed_by']['edges']]
                    
                    for edge in user_data['edge_owner_to_timeline_media']['edges']:
                        post = edge['node']
                        profile_data['posts'].append({
                            'link': f"https://www.instagram.com/p/{post['shortcode']}/",
                            'title': post['edge_media_to_caption']['edges'][0]['node']['text'] if post['edge_media_to_caption']['edges'] else 'N/A',
                            'description': post['edge_media_to_caption']['edges'][0]['node']['text'] if post['edge_media_to_caption']['edges'] else 'N/A',
                            'hashtags': [tag['name'] for tag in post['tags']],
                            'tags': [tag['username'] for tag in post['tagged_users']],
                            'location': post['location']['name'] if post['location'] else 'N/A'
                        })
                    break
            return profile_data
        else:
            # Placeholder for other platforms
            print("Only Instagram is supported in this example.")
            return None
    except Exception as e:
        print(f"Error fetching profile data: {e}")
        return None

def save_post_info_to_file(profile_data, filename):
    with open(filename, 'w') as file:
        file.write(f"Profile Photo: {profile_data['profile_pic_url']}\n")
        file.write(f"Following: {', '.join(profile_data['following'])}\n")
        file.write(f"Followers: {', '.join(profile_data['followers'])}\n\n")
        
        for post in profile_data['posts']:
            file.write(f"Post Link: {post['link']}\n")
            file.write(f"Title: {post.get('title', 'N/A')}\n")
            file.write(f"Description: {post.get('description', 'N/A')}\n")
            file.write(f"Hashtags: {', '.join(post.get('hashtags', []))}\n")
            file.write(f"Tags: {', '.join(post.get('tags', []))}\n")
            file.write(f"Location: {post.get('location', 'N/A')}\n\n")
    
    print(f"Post information saved to '{filename}'")

def perform_security_analysis(profile):
    vulnerabilities = []
    return vulnerabilities

def generate_report(vulnerabilities):
    report = {
        'summary': f'Found {len(vulnerabilities)} vulnerabilities.',
        'details': vulnerabilities
    }
    return report

def clone_and_analyze_profile(url, platform, cloning_choice):
    profile_data = fetch_profile_data(url, platform)
    
    if profile_data is None:
        print("Failed to fetch profile data.")
        return

    if cloning_choice == '1':
        save_post_info_to_file(profile_data, 'post_info.txt')
    elif cloning_choice == '2':
        assassin_username = input("Enter the Assassin account username or email: ")
        assassin_password = getpass.getpass("Enter the Assassin account password: ")
        try:
            if False:
                raise ValueError("Invalid credentials")
            vulnerabilities = perform_security_analysis(profile_data)
            report = generate_report(vulnerabilities)
            print('ALPHA-CLONE Report')
            print('=================')
            print(report['summary'])
            for detail in report['details']:
                print(detail)
        except ValueError as e:
            print(str(e))
    else:
        raise ValueError("Unsupported cloning choice")

def main():
    display_startup_message()

    print("Choose the target platform:")
    print("1. Instagram")
    print("2. Facebook Account")
    print("3. Facebook Page")
    print("4. LinkedIn Profile")
    platform_choice = input("Enter the number of your choice: ")

    profile_url = input("Enter the account URL or username: ")

    print("Choose the cloning method:")
    print("1. Manual Cloning")
    print("2. Automated Cloning")
    cloning_choice = input("Enter the number of your choice: ")

    try:
        clone_and_analyze_profile(profile_url, platform_choice, cloning_choice)
    except ValueError as e:
        print(str(e))

if __name__ == '__main__':
    main()
