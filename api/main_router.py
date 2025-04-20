from fastapi import APIRouter
from .handlers.comparison_history import get_comparison_history
from .handlers.create_comparison import create_comparison
from .handlers.save_comparison import save_comparison_handler

router = APIRouter(prefix="/api/comparison", tags=["comparison"])
router.add_api_route("/", create_comparison, methods=["POST"])
router.add_api_route("/save", save_comparison_handler, methods=["POST"])
router.add_api_route("/history", get_comparison_history, methods=["GET"])