from backend.app import create_app

app = create_app()

with app.app_context():
    print("Available routes:")
    for rule in app.url_map.iter_rules():
        print(f"  {rule.rule} -> {rule.endpoint}")