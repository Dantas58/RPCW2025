# TPC 2

Queries em SPARQL 

### 1 - Quantos triplos existem na topologia?

```
PREFIX : <http://www.semanticweb.org/andre/ontologies/2015/6/historia#>
SELECT (COUNT(?s) AS ?totalTriplos) WHERE {
  ?s ?p ?o .
}
```

### 2 - Que classes estão definidas?

```
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX : <http://www.semanticweb.org/andre/ontologies/2015/6/historia#>
SELECT ?c WHERE {
    ?c rdf:type owl:Class.
}
```

### 3 - Que propriedades tem a classe "Rei"?

```
PREFIX : <http://www.semanticweb.org/andre/ontologies/2015/6/historia#>
SELECT DISTINCT ?p WHERE {
    ?s a :Rei .
    ?s ?p ?o .
}
```

### 4 - Quantos reis aparecem na ontologia?

```
PREFIX : <http://www.semanticweb.org/andre/ontologies/2015/6/historia#>
SELECT (COUNT(DISTINCT ?s) AS ?nReis) WHERE{
    ?s a :Rei .
}
```

### 5 - Calcula uma tabela com o seu nome, data de nascimento e cognome.

```
PREFIX : <http://www.semanticweb.org/andre/ontologies/2015/6/historia#>
SELECT ?s ?n ?data ?c WHERE {
    ?s a :Rei .
    ?s :nome ?n.
    ?s :nascimento ?data.
    ?s :cognomes ?c.
} 
```

### 6 - Acrescenta à tabela anterior a dinastia em que cada rei reinou.

```
PREFIX : <http://www.semanticweb.org/andre/ontologies/2015/6/historia#>
SELECT ?n ?data ?c ?d WHERE {
    ?s a :Rei .
    ?s :nome ?n .
    ?s :nascimento ?data .
    ?s :cognomes ?c .
    ?s :temReinado ?reinado .
    ?reinado :dinastia ?dinastia .
    ?dinastia :nome ?d
}
```


### 7 - Qual a distribuição de reis pelas 4 dinastias?

```
PREFIX : <http://www.semanticweb.org/andre/ontologies/2015/6/historia#>
SELECT ?d (COUNT(DISTINCT ?s) AS ?nReis)
WHERE {
    ?s a :Rei .
    ?s :temReinado ?reinado .
    ?reinado :dinastia ?d .
}
GROUP BY ?d
ORDER BY DESC(?nReis)
```

### 8 - Lista de descobrimentos (sua descrição) por ordem cronológica.

```
PREFIX : <http://www.semanticweb.org/andre/ontologies/2015/6/historia#>
SELECT ?desc ?data WHERE{
    ?s a :Descobrimento .
    ?s :data ?data .
    ?s :notas ?desc .
}ORDER BY (?data)
```

### 9 - Lista as várias conquista, nome e data, com o nome do rei que reinava no momento.

```
PREFIX : <http://www.semanticweb.org/andre/ontologies/2015/6/historia#>
SELECT ?n ?data ?r WHERE{
    ?s a :Conquista .
    ?s :nome ?n .
    ?s :data ?data .
    ?s :temReinado ?d .
    ?dinastia :temMonarca ?nRei .
    ?nRei :nome ?r .
}ORDER BY (?data)
```

### 10 - Calcula uma tabela com o nome, data de nascimento e número de mandatos de todos os presidentes portugueses.

```
PREFIX : <http://www.semanticweb.org/andre/ontologies/2015/6/historia#>
SELECT ?n ?data (count(?mandato) as ?nMandato) WHERE{
    ?s a :Presidente .
    ?s :nome ?n . 
    ?s :nascimento ?data .
    ?s :mandato ?mandato .
}GROUP BY ?s ?n ?data
```

### 11 - Quantos mandatos teve o presidente Sidónio Pais? Em que datas começaram e terminaram esses mandatos?

```
PREFIX : <http://www.semanticweb.org/andre/ontologies/2015/6/historia#>
SELECT ?mandato ?i ?f WHERE {
    ?presidente :nome "Sidónio Bernardino Cardoso da Silva Pais" .
    ?presidente :mandato ?mandato .
    ?mandato :comeco ?i .
    ?mandato :fim ?f .
}
```


### 12 - Quais os nomes dos partidos políticos na ontologia?

```
PREFIX : <http://www.semanticweb.org/andre/ontologies/2015/6/historia#>
SELECT ?n WHERE {
    ?s a :Partido .
    ?s :nome ?n .
}
```


### 13 - Qual a distribuição dos militantes por cada partido político?

```
PREFIX : <http://www.semanticweb.org/andre/ontologies/2015/6/historia#>
SELECT ?n (COUNT(?m) AS ?numMilitantes) WHERE {
    ?partido a :Partido .
    ?partido :nome ?n .
    ?partido :temMilitante ?m .
}GROUP BY (?n)
```

### 14 - Qual o partido com maior número de presidentes militantes?

```
PREFIX : <http://www.semanticweb.org/andre/ontologies/2015/6/historia#>
SELECT ?n (COUNT(?m) AS ?numMilitantes) WHERE {
    ?partido a :Partido .
    ?partido :nome ?n .
    ?partido :temMilitante ?m .
}GROUP BY (?n)
ORDER BY DESC (?numMilitantes)
LIMIT 1 
```