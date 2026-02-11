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
            'user': request.user.username if request.user.is_authenticated else 'Anonymous',
        }

        logger.info(f"API Access: {log_data}")

        return response


class SecurityHeadersMiddleware:
    """Adiciona cabeçalhos de segurança padrão nas respostas HTTP."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
        response['Cross-Origin-Opener-Policy'] = 'same-origin'

        if request.is_secure():
            response['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'

        return response
