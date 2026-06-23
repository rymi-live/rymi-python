import hmac
import hashlib
import time

class WebhooksUtility:
    """Secure Utility for Webhook Signature Verification."""

    @staticmethod
    def verify_signature(
        payload: str,
        signature_header: str,
        timestamp_header: str,
        webhook_secret: str,
        tolerance_millis: int = 300000 # 5 minutes
    ) -> bool:
        """
        Verifies that a webhook received by your backend was genuinely dispatched by Rymi.
        
        Rymi endpoints secure webhooks by computing an HMAC-SHA256 signature
        of the raw JSON body concatenated with the timestamp using your Webhook Secret.
        """
        # 1. Check for Replay Attacks
        try:
            timestamp = int(timestamp_header)
        except ValueError:
            raise ValueError("Invalid Rymi-Timestamp header format.")
            
        current_time = int(time.time() * 1000)
        if (current_time - timestamp) > tolerance_millis:
            raise ValueError("Webhook timestamp is too old. Possible replay attack.")
            
        # 2. Prepare the verification string
        signature_payload = f"{timestamp}.{payload}"
        
        # 3. Compute expected HMAC
        expected_signature = hmac.new(
            webhook_secret.encode('utf-8'),
            signature_payload.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        # 4. Secure string comparison
        if not hmac.compare_digest(signature_header, expected_signature):
            raise ValueError("Invalid Webhook Signature. The secret might be incorrect.")
            
        return True
