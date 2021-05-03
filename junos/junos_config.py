from jnpr.junos.utils.config import Config
from jnpr.junos.exception import ConfigLoadError, CommitError, ConnectAuthError, ConnectTimeoutError
from jnpr.junos import Device


def junos_config(host=None, user=None, password=None, port=830, auto_probe=30, set_cmds=None, commit=True):
    try:
        dev = Device(
            host=host,
            user=user,
            password=password,
            port=port,
            auto_probe=auto_probe
        )
        dev.open()
        conf = Config(dev)
        conf.lock()
        conf.load(set_cmds, format='set')
        if commit and conf.diff():
            result = conf.diff()
            conf.commit()
            result += "\n\n Nova configuração aplicada."
            conf.unlock()
        elif not commit:
            result = conf.diff()
            conf.rollback()
            conf.unlock()
            result += "\n\n Esta configuração não sera aplicada."
        else:
            result = "Configuração já está atualizada."
            conf.unlock()
    except ConnectAuthError:
        result = "Erro de autenticação!"
    except ConnectTimeoutError:
        result = "Conexão NETCONF atingiu o tempo limite de conexão!"
    except (ConfigLoadError, CommitError) as err:
        result = f"Problema ao carregar nova configuração: {err}"
    except Exception as err:
        result = f"Erro: {err}"
    finally:
        dev.close()
    return result
