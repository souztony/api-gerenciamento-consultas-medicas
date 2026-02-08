import logging

logger = logging.getLogger('django')

class AsaasService:
    """
    Mock service para integração com a API da Asaas.
    Demonstra como o split de pagamento seria realizado.
    """
    
    @staticmethod
    def create_payment_with_split(appointment):
        """
        Simula a criação de uma cobrança com split de pagamento.
        """
        professional = appointment.professional
        
        # Dados fictícios para demonstração do payload da Asaas
        payload = {
            "customer": "customer_id_da_lacrei",
            "billingType": "CREDIT_CARD",
            "value": 200.0,
            "dueDate": appointment.date.strftime("%Y-%m-%d"),
            "description": f"Consulta com {professional.social_name} em {appointment.date}",
            "split": [
                {
                    "walletId": "wallet_id_do_profissional", # ID da conta do profissional na Asaas
                    "fixedValue": 180.0, # Valor que vai para o profissional
                },
                {
                    "walletId": "wallet_id_da_lacrei", # ID da conta da Lacrei Saúde
                    "fixedValue": 20.0, # Taxa da plataforma
                }
            ]
        }
        
        logger.info(f"Asaas Mock: Cobrança criada para Consulta #{appointment.id}. Payload: {payload}")
        
        # Em uma integração real, aqui faríamos um requests.post para a API da Asaas
        return {"status": "success", "asaas_id": "pay_123456789"}
