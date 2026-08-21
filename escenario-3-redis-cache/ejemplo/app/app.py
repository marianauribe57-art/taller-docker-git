from flask import Flask, jsonify
import redis
import time
import os

app = Flask(__name__)

# Conexión a Redis
redis_client = redis.Redis(
    host=os.environ.get('REDIS_HOST', 'redis'),
    port=os.environ.get('REDIS_PORT', 6379),
    decode_responses=True
)

def obtener_datos_lentos():
    """Simula una operación que toma 3 segundos (ej: query pesada a BD)"""
    time.sleep(3)
    return {"mensaje": "Datos procesados", "timestamp": time.time()}

@app.route('/')
def index():
    return jsonify({"servicio": "App con cache Redis", "status": "activo"})

@app.route('/datos')
def obtener_datos():
    cache_key = "datos_cache"

    # Intentar obtener de caché
    datos_cache = redis_client.get(cache_key)
    if datos_cache:
        return jsonify({
            "origen": "cache",
            "datos": eval(datos_cache),
            "ttl_restante": redis_client.ttl(cache_key)
        })

    # Si no está en caché, obtener datos "lentos"
    datos = obtener_datos_lentos()

    # Guardar en caché por 60 segundos
    redis_client.setex(cache_key, 60, str(datos))

    return jsonify({
        "origen": "base_de_datos",
        "datos": datos,
        "cacheado_por": "60 segundos"
    })

@app.route('/cache/estadisticas')
def estadisticas_cache():
    info = redis_client.info()
    return jsonify({
        "keys_totales": redis_client.dbsize(),
        "memoria_usada": info.get('used_memory_human'),
        "hits": info.get('keyspace_hits'),
        "misses": info.get('keyspace_misses')
    })

@app.route('/cache/limpiar')
def limpiar_cache():
    redis_client.flushdb()
    return jsonify({"mensaje": "Cache limpiada exitosamente"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)