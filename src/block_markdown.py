try:
    from markdown_blocks import (
        BlockType,
        block_to_block_type,
        markdown_to_blocks,
        markdown_to_html_node,
    )
except ImportError:
    from src.markdown_blocks import (
        BlockType,
        block_to_block_type,
        markdown_to_blocks,
        markdown_to_html_node,
    )
