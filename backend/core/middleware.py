import logging
import time

logger = logging.getLogger('django')

class RequestLoggingMiddleware:
    """
    Middleware para registrar logs de cada requisição (método, path, status, tempo de execução).
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        
        response = self.get_response(request)
        
        duration = time.time() - start_time
        
        # Obter IP do cliente
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        # Logar detalhes da requisição
        log_data = {
            'method': request.method,
            'path': request.get_full_path(),
            'status': response.status_code,
            'duration': f"{duration:.3f}s",
            'ip': ip,
            'user': request.user.username if request.user.is_authenticated else 'Anonymous'
        }
        
        logger.info(f"API Access: {log_data}")
        
        return response
