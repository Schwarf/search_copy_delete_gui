def format_size(size_bytes: int) -> str:
    power = 1024
    n = 0
    size_labels = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
    while size_bytes > power:
        size_bytes /= power
        n += 1
    return f"{size_bytes:.2f} {size_labels[n]}"
