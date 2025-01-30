from banco import criar_conexao

conexao = criar_conexao()
if conexao:
    print("✅ Conexão com MySQL bem-sucedida!")
    conexao.close()
else:
    print("❌ Falha na conexão. Verifique:")
    print("- Servidor MySQL está rodando?")
    print("- Credenciais no database.py estão corretas?")
    print("- O banco 'locadora' foi criado?")