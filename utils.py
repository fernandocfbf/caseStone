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
    
    #filtra para chamados meses antes
    df_cliente_before = df_cliente.loc[(df_cliente["time_distance"] <= 150) & (df_cliente["time_distance"] > 0)]
    table_before = df_cliente_before[["count", "mes_x"]].groupby(["mes_x"]).sum()
    
    #filtra para meses depois
    df_cliente_after = df_cliente.loc[(df_cliente["time_distance"] >= -30) & (df_cliente["time_distance"] <= 0)]
    table_after = df_cliente_after[["count", "mes_x"]].groupby(["mes_x"]).sum()
    
    #se não teve nenhum chamado antes
    if(table_before.shape[0] == 0):
        before = 0
    else:
        before = table_before.mean()[0]
        
    #se não teve nenhum chamado depois
    if(table_after.shape[0] == 0):
        after = 0
    else:
        after = table_after.mean()[0]
    
    return [before, after]