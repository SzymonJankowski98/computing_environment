REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework_api_key.permissions.HasAPIKey",
    ]
}

API_KEY_CUSTOM_HEADER = "HTTP_X_API_KEY"
