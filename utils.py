def get_cred_date(client_id, check_list, creds):
    """
    Função responsável por pegar a data de credenciamento para determinado cliente
    Parâmetros: id do cliente (string), lista de id credenciados (list), base de credenciamento (Pandas.DataFrame)
    Retorna: Data do credenciamento se existir e "nao credenciado" caso não exista
    """
    if client_id in check_list:
        return creds.loc[creds["accountid"] == client_id]["cred_date"].tolist()[0]
    return 'nao credenciado'

def get_5months_before(client_id, df):
    """
    Função reposável por calcular a média de atendimentos dois meses antes do credenciamento
    Recebe: id do cliente (string), data de credenciamento (datetime), base de dados total (Pandas.Dataframe)
    """
    
    #filtra somente para o cliente desejado
    df_cliente = df.loc[df["accountid"] == client_id]
    
    mes_cred = df_cliente["cred_date"].tolist()[0] #mes do credenciamento
    
    #filtra para chamados meses antes
    df_cliente_before = df_cliente.loc[(df_cliente["date_ref"].month >= mes_cred-5) & (df_cliente["date_ref"].month < mes_cred)]
    
    #filtra para mes do credenciamento
    df_cliente_after = df_cliente.loc[df_cliente["date_ref"].month == mes_cred]
    
    #se não teve nenhum chamado antes
    if(df_cliente_before.shape[0] == 0):
        before = 0
    else:
        before = df_cliente_before['count'].sum()/5
        
    #se não teve nenhum chamado depois
    if(df_cliente_after.shape[0] == 0):
        after = 0
    else:
        after = df_cliente_after['count'].sum()
    
    return [before, after]