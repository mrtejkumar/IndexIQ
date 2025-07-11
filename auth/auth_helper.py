import streamlit_authenticator as stauth
import yaml
from pathlib import Path

def load_authenticator():
    """Load authenticator configuration"""
    config_path = Path(__file__).parent / "auth_config.yaml"
    
    # Create default config if it doesn't exist
    if not config_path.exists():
        default_config = {
            'credentials': {
                'usernames': {}
            },
            'cookie': {
                'expiry_days': 30,
                'key': 'indexiq_auth_key',
                'name': 'indexiq_auth_cookie'
            }
        }
        
        # Ensure directory exists
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        with config_path.open("w") as f:
            yaml.dump(default_config, f, default_flow_style=False)
    
    # Load config
    with config_path.open("r") as f:
        config = yaml.safe_load(f)
    
    # Create authenticator without deprecated parameters
    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days']
    )
    
    return authenticator, config

def save_config(config):
    """Save configuration to file"""
    config_path = Path(__file__).parent / "auth_config.yaml"
    with config_path.open("w") as f:
        yaml.dump(config, f, default_flow_style=False)