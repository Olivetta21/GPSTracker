-- Postgresql
-- versão: 0.2
-- em homologação


create table legal_ident_tipo   (
    id serial primary key,
    descricao varchar(100) not null,
    regex varchar(200) not null,
    invalido boolean not null default false
);

create table legal_ident (
    id serial primary key,
    tipo_id integer not null references legal_ident_tipo(id),
    identidade varchar(100) not null
);

create table usuario (
    id serial primary key,
    nome varchar(100) not null,
    login varchar(100),
    senha varchar(100), --sem criptografia por enquanto
    legal_ident_id integer not null references legal_ident(id),
    ativo boolean not null default true,
    email varchar(100),
    telefone varchar(15),
    token varchar(16)
);

create view vw_usuario as
    select
        u.id, u.nome, u.login, u.email, u.telefone,
        li.tipo_id, li.identidade
    from usuario as u
    join legal_ident as li on li.id = u.legal_ident_id
    where u.ativo = true;

create table administrador (
    id integer primary key references usuario(id)
);

create table rastreador (
    id serial primary key,
    hardware varchar(100),
    token varchar(100) not null,
    token_publico varchar(100) not null,
    senha varchar(100), --sem criptografia por enquanto
    obs varchar(200),
    status integer not null,
    ativo boolean not null default true,
    dono_id integer not null references usuario(id)
);

create view vw_rastreador as
    select id, token_publico, status, dono_id
    from rastreador
    where ativo = true;

create table usuario_rastreador (
    id serial primary key,
    usuario_id integer not null references usuario(id),
    rastreador_id integer not null references rastreador(id),
    nome varchar(100) not null,
    status integer not null,
    ativo boolean not null default true,
    loc_temporeal boolean not null default true,
    loc_salvos boolean not null default true
);

-- Pegar todos os vinculos de rastreadores e usuarios
create view vw_usuario_rastreador as
    select
        ur.id as ur_id, ur.usuario_id as u_id, ur.nome, ur.status as ur_status, ur.loc_temporeal, ur.loc_salvos,
        r.id as r_id, r.token_publico, r.dono_id, r.status as r_status
    from usuario_rastreador as ur
    join rastreador as r on r.id = ur.rastreador_id
    join usuario as u on u.id = ur.usuario_id
    where ur.ativo = true
        and r.ativo = true
        and u.ativo = true;

create table localizacao (
    id serial primary key,
    rastreador_id integer not null references rastreador(id),
    lat double precision not null,
    lng double precision not null,
    data timestamp not null,
    invalida boolean not null default false
);

create table intervalo_loc_oculta (
    id serial primary key,
    usuario_rastreador_id integer not null references usuario_rastreador(id),
    id_inicial integer,
    id_final integer,
    data_inicial timestamp,
    data_final timestamp
);

-- Permissões de usuario
create table permissao_usuario (
    id serial primary key,
    nome varchar(100) not null
);
create table grupo_usuario (
    id serial primary key,
    nome varchar(100) not null
);
create table vinc_grupo_usuario (
    id serial primary key,
    usuario_id integer not null references usuario(id),
    grupo_id integer not null references grupo_usuario(id)
);
create table vinc_perm_usuario (
    id serial primary key,
    grupo_id integer references grupo_usuario(id),
    usuario_id integer references usuario(id),
    perm_id integer not null references permissao_usuario(id),
    negado boolean not null default false
);
-- Ver permissoes do grupo
create view vw_permissoes_grupo_usuario as
    select gu.id as grupo_id, vpu.perm_id, vpu.negado
    from grupo_usuario gu
    join vinc_perm_usuario vpu on vpu.grupo_id = gu.id;
-- Ver permissoes do usuario
create view vw_permissoes_usuario as
	select usuario_id, perm_id, CASE WHEN COUNT(*) > 1 THEN TRUE ELSE FALSE END AS negado
	from (
		select usuario_id, perm_id, negado from (
		    select vpu.usuario_id, vpu.perm_id, vpu.negado
		    from vinc_perm_usuario vpu
			where usuario_id is not null
		    union all
		    select vgu.usuario_id, vpu.perm_id, vpu.negado
			from vinc_grupo_usuario vgu
			join vinc_perm_usuario vpu on vpu.grupo_id = vgu.grupo_id
		) group by usuario_id, perm_id, negado
	)
	group by usuario_id, perm_id;


select * from vw_permissoes_usuario order by usuario_id, perm_id;
select * from vw_permissoes_grupo_usuario;




-- Permisões de rastreador
create table permissao_rastreador (
    id serial primary key,
    nome varchar(100) not null
);
create table grupo_rastreador (
    id serial primary key,
    nome varchar(100) not null
);
create table vinc_grupo_rastreador (
    id serial primary key,
    rastreador_id integer not null references rastreador(id),
    grupo_id integer not null references grupo_rastreador(id)
);
create table vinc_perm_rastreador (
    id serial primary key,
    grupo_id integer references grupo_rastreador(id),
    rastreador_id integer references rastreador(id),
    perm_id integer not null references permissao_rastreador(id),
    negado boolean not null default false
);
-- Permissoes do grupo rastreador
create view vw_permissoes_grupo_rastreador as
    select gr.id as grupo_id, vpr.perm_id, vpr.negado
    from grupo_rastreador gr
    join vinc_perm_rastreador vpr on vpr.grupo_id = gr.id;
-- Permissoes do rastreador
create view vw_permissoes_rastreador as
    select rastreador_id, perm_id, CASE WHEN COUNT(*) > 1 THEN TRUE ELSE FALSE END AS negado
    from (
        select rastreador_id, perm_id, negado from (
            select vpr.rastreador_id, vpr.perm_id, vpr.negado
            from vinc_perm_rastreador vpr
            where rastreador_id is not null
            union all
            select vgr.rastreador_id, vpr.perm_id, vpr.negado
            from vinc_grupo_rastreador vgr
            join vinc_perm_rastreador vpr on vpr.grupo_id = vgr.grupo_id
        ) group by rastreador_id, perm_id, negado
    )
    group by rastreador_id, perm_id;


select * from vw_permissoes_rastreador order by rastreador_id, perm_id;
select * from vw_permissoes_grupo_rastreador;













-- Pegar todos os ouvintes de um rastreador específico, a consulta está sendo feita pelo dono do rastreador
-- Terá que usar função para melhor desempenho
create function fn_ouvintes_rastreador(rastreador_id_input integer, dono_id_input integer)
returns table (
    usuario_id integer,
    status integer,
    loc_temporeal boolean,
    loc_salvos boolean,
    nome varchar(100)
) as $$
    declare
        var_rastreador_id integer;
    begin
        -- Verifica se o rastreador existe e pertence ao dono
        select r.id into var_rastreador_id from vw_rastreador r
        where r.id = rastreador_id_input
        and r.dono_id = dono_id_input;
        -- retorna se não encontrar
        if not found or var_rastreador_id is null then
            return;
        end if;

        -- Pega os ouvintes do rastreador
        return query
        select
            ur.usuario_id, ur.status, ur.loc_temporeal, ur.loc_salvos,
            u.nome
        from usuario_rastreador as ur
        join usuario as u on u.id = ur.usuario_id
        where ur.rastreador_id = var_rastreador_id
        and ur.usuario_id != dono_id_input
        and ur.ativo = true
        and u.ativo = true;
    end;
$$ language plpgsql;





-- Todas as localizações salvas permitidas de um rastreador específico
-- Terá que usar função para melhor desempenho
create function fn_loc_salvas_permitidas(rastreador_id_input integer, usuario_id_input integer)
returns table (
    id integer,
    lat double precision,
    lng double precision,
    data timestamp,
    invalida boolean
) as $$
    declare
        var_ur_id integer;
    begin
        -- Verifica se o rastreador existe e o usuario tem esse rastreador registrado, e guarda o id para usar no filtro
        select ur.ur_id into var_ur_id from vw_usuario_rastreador ur
        where ur.r_id = rastreador_id_input
        and ur.u_id = usuario_id_input;
        -- retorna se não encontrar
        if not found or var_ur_id is null then
            return;
        end if;

        -- Pega as localizações salvas já excluindo os filtros
        return query
        select l.id, l.lat, l.lng, l.data, l.invalida
        from localizacao as l
        where l.rastreador_id = rastreador_id_input
        and not exists (
            select 1 from intervalo_loc_oculta as f --filtro
            where f.usuario_rastreador_id = var_ur_id
            and (
                (l.data >= f.data_inicial and l.data <= f.data_final) or
                (l.id >= f.id_inicial and l.id <= f.id_final)
            )
        );
    end;
$$ language plpgsql;





insert into legal_ident_tipo (descricao, regex) values ('Geral', '.+');
insert into legal_ident (tipo_id, identidade) values (1, '123456789');

insert into usuario (nome, login, senha, legal_ident_id) values ('Dono Exemplo', 'donoexemplo', '123', 1);
insert into usuario (nome, login, senha, legal_ident_id) values ('Ouvinte Exemplo', 'ouvinteexemplo', '123', 1);
insert into usuario (nome, login, senha, legal_ident_id) values ('Maria Silva', 'mariasilva', 'senha456', 1);
insert into usuario (nome, login, senha, legal_ident_id) values ('Carlos Pereira', 'carlospereira', 'senha789', 1);
insert into usuario (nome, login, senha, legal_ident_id) values ('Ana Oliveira', 'anaoliveira', 'senha321', 1);

insert into rastreador (hardware, token, token_publico, senha, obs, status, dono_id) values ('Rastreador Exemplo', 'token123', 'token_publico123', 'senha123', 'Observações sobre o rastreador', 55, 1);
insert into rastreador (hardware, token, token_publico, senha, obs, status, dono_id) values ('Rastreador Alpha', 'tokenAlpha123', 'tokenPublicoAlpha123', 'senhaAlpha123', 'Rastreador de teste', 1, 2);
insert into rastreador (hardware, token, token_publico, senha, obs, status, dono_id) values ('Rastreador Beta', 'tokenBeta456', 'tokenPublicoBeta456', 'senhaBeta456', 'Monitoramento em tempo real', 2, 3);
insert into rastreador (hardware, token, token_publico, senha, obs, status, dono_id) values ('Rastreador Gamma', 'tokenGamma789', 'tokenPublicoGamma789', 'senhaGamma789', 'Acompanhamento de veículos', 2, 4);

insert into usuario_rastreador (usuario_id, rastreador_id, nome, status) values (1, 1, 'Meu Rastreador', 44);
insert into usuario_rastreador (usuario_id, rastreador_id, nome, status) values (2, 1, 'Rastreador do Dono Exemplo', 44);
insert into usuario_rastreador (usuario_id, rastreador_id, nome, status) values (1, 2, 'Rastreador Alpha', 12);
insert into usuario_rastreador (usuario_id, rastreador_id, nome, status) values (2, 1, 'Rastreador Beta', 15);
insert into usuario_rastreador (usuario_id, rastreador_id, nome, status) values (3, 3, 'Rastreador Gamma', 10);
insert into usuario_rastreador (usuario_id, rastreador_id, nome, status) values (4, 2, 'Rastreador Beta', 9);

insert into localizacao (rastreador_id, lat, lng, data) values (1, -23.55052, -46.633308, '2024-01-01 10:00:00');
insert into localizacao (rastreador_id, lat, lng, data) values (1, -23.55100, -46.634000, '2024-01-01 11:00:00');
insert into localizacao (rastreador_id, lat, lng, data) values (1, -23.55100, -46.634000, '2024-12-01 11:00:00');
insert into localizacao (rastreador_id, lat, lng, data) values (1, -23.55052, -46.633308, '2024-01-02 10:30:00');
insert into localizacao (rastreador_id, lat, lng, data) values (2, -22.908333, -43.196388, '2024-01-02 11:00:00');
insert into localizacao (rastreador_id, lat, lng, data) values (3, -25.444444, -49.275000, '2024-01-02 11:30:00');
insert into localizacao (rastreador_id, lat, lng, data) values (2, -23.567890, -46.6789410, '2024-01-02 12:00:00');
insert into localizacao (rastreador_id, lat, lng, data) values (3, -21.567890, -46.6789710, '2024-01-02 12:00:00');
insert into localizacao (rastreador_id, lat, lng, data) values (1, -23.4890, -46.6789100, '2024-01-02 12:00:00');
insert into localizacao (rastreador_id, lat, lng, data) values (3, -23.1890, -46.6789102, '2024-01-02 12:00:00');
insert into localizacao (rastreador_id, lat, lng, data) values (4, -23.87590, -46.6781370, '2024-01-02 12:00:00');
insert into localizacao (rastreador_id, lat, lng, data) values (1, -23.89750, -46.6789150, '2024-01-02 12:00:00');
insert into localizacao (rastreador_id, lat, lng, data) values (3, -23.8930, -46.6789170, '2024-01-02 12:00:00');
insert into localizacao (rastreador_id, lat, lng, data) values (2, -23.892130, -46.6728910, '2024-01-02 12:00:00');
insert into localizacao (rastreador_id, lat, lng, data) values (2, -23.89230, -46.6789610, '2024-01-02 12:00:00');
insert into localizacao (rastreador_id, lat, lng, data) values (2, -23.89560, -46.66478910, '2024-01-02 12:00:00');

insert into intervalo_loc_oculta (usuario_rastreador_id, data_inicial, data_final) values (2, '2024-12-01 00:00:00', '2024-12-31 23:59:59');
insert into intervalo_loc_oculta (usuario_rastreador_id, id_inicial, id_final) values (1, 2, 2);
insert into intervalo_loc_oculta (usuario_rastreador_id, data_inicial, data_final) values (1, '2024-11-01 00:00:00', '2024-11-15 23:59:59');
insert into intervalo_loc_oculta (usuario_rastreador_id, data_inicial, data_final) values (2, '2024-11-10 00:00:00', '2024-11-20 23:59:59');
insert into intervalo_loc_oculta (usuario_rastreador_id, data_inicial, data_final) values (3, '2024-12-01 00:00:00', '2024-12-15 23:59:59');
insert into intervalo_loc_oculta (usuario_rastreador_id, data_inicial, data_final) values (4, '2024-12-05 00:00:00', '2024-12-10 23:59:59');


insert into permissao_usuario (nome) values ('Login');
insert into permissao_usuario (nome) values ('Ver Mapa');
insert into permissao_usuario (nome) values ('Registrar Rastreador');
insert into permissao_usuario (nome) values ('Modificar Rastreador');
insert into permissao_usuario (nome) values ('Modificar Perfil');
insert into permissao_usuario (nome) values ('Transferir Posse');
insert into permissao_usuario (nome) values ('Gerenciar ouvintes');
insert into permissao_usuario (nome) values ('Rastreio Salvo');
insert into permissao_usuario (nome) values ('Rastreio T.R.');
insert into permissao_usuario (nome) values ('Quer Propostas Rastreio');
insert into permissao_usuario (nome) values ('Proposta Rastreio');
insert into permissao_usuario (nome) values ('Intervalo Oculto');
insert into permissao_usuario (nome) values ('Desativar Rastreador');
insert into permissao_rastreador (nome) values ('Conexão');
insert into permissao_rastreador (nome) values ('Enviar Localização');
insert into permissao_rastreador (nome) values ('Resgistrável');
insert into permissao_rastreador (nome) values ('Rastreável R.T');
insert into permissao_rastreador (nome) values ('Rastreável');
insert into permissao_rastreador (nome) values ('Ouvintes');
insert into grupo_usuario (nome) values ('Grupo Usuario 1');
insert into grupo_usuario (nome) values ('Grupo Usuario 2');
insert into grupo_rastreador (nome) values ('Grupo Rastreador A');
insert into grupo_rastreador (nome) values ('Grupo Rastreador B');
insert into vinc_grupo_usuario (usuario_id, grupo_id) values (1, 1); -- usuario 1 no grupo 1
insert into vinc_grupo_usuario (usuario_id, grupo_id) values (1, 2); -- usuario 1 no grupo 2
insert into vinc_grupo_usuario (usuario_id, grupo_id) values (3, 1); -- usuario 3 no grupo 1
insert into vinc_grupo_usuario (usuario_id, grupo_id) values (3, 2); -- usuario 3 no grupo 2
insert into vinc_grupo_usuario (usuario_id, grupo_id) values (5, 1); -- usuario 5 no grupo 1
insert into vinc_grupo_rastreador (rastreador_id, grupo_id) values (1, 1); -- rastreador 1 no grupo 1
insert into vinc_perm_usuario (grupo_id, perm_id, negado) values (1, 1, false);
insert into vinc_perm_usuario (grupo_id, perm_id, negado) values (1, 2, false);
insert into vinc_perm_usuario (grupo_id, perm_id, negado) values (1, 3, false);
insert into vinc_perm_usuario (grupo_id, perm_id, negado) values (1, 4, false);
insert into vinc_perm_usuario (grupo_id, perm_id, negado) values (2, 1, false);
insert into vinc_perm_usuario (grupo_id, perm_id, negado) values (2, 2, true);
insert into vinc_perm_usuario (grupo_id, perm_id, negado) values (2, 4, true);
insert into vinc_perm_usuario (usuario_id, perm_id, negado) values (1, 5, false); -- usuario 1 perm de 1 a 4 do grupo mais a 5 individual
insert into vinc_perm_usuario (usuario_id, perm_id, negado) values (2, 3, false);
insert into vinc_perm_usuario (usuario_id, perm_id, negado) values (3, 4, true); -- nega permissão 4 para usuario 3
insert into vinc_perm_usuario (usuario_id, perm_id, negado) values (4, 5, false);
insert into vinc_perm_usuario (usuario_id, perm_id, negado) values (5, 1, false);
insert into vinc_perm_usuario (usuario_id, perm_id, negado) values (5, 2, false);
insert into vinc_perm_usuario (usuario_id, perm_id, negado) values (5, 3, false);
insert into vinc_perm_usuario (usuario_id, perm_id, negado) values (5, 4, false);
insert into vinc_perm_usuario (usuario_id, perm_id, negado) values (5, 5, false);
insert into vinc_perm_usuario (usuario_id, perm_id, negado) values (5, 6, false);
insert into vinc_perm_rastreador (grupo_id, perm_id, negado) values (1, 1, false);
