# Sturpy - A versão resiliente do Python

## Visão Geral
Apesar de ser uma das linguagens mais utilizadas no mundo, o Python possui um problema. Ela é uma linguagem leniente - não há muita coisa que o compilador não aceite. O que parece uma benção para programadores iniciantes se transforma em um pesadelo à medida que um projeto escala. Com cada um escrevendo da sua própria maneira, o risco é acabar com um código remendado, pouco legível e, portanto, de difícil manutenção. Devido a isso, normas e boas práticas se tornaram de extremo valor para projetos complexos. Mas nunca houve uma forma de tornar isso obrigatório - até agora.

**Sturpy** é uma linguagem de programação baseada em Python que introduz duas mudanças significativas:

 - **Tipagem Forte Exclusiva**: Em Nome da Linguagem de Programação, todas as variáveis são exclusivamente fortemente tipadas. Isso significa que você deve declarar explicitamente o tipo de uma variável e, uma vez definido, esse tipo não pode ser alterado.

 - **Normas PEP 8 Obrigatórias**: Adotamos e incentivamos o uso estrito das normas definidas no PEP 8 (Python Enhancement Proposal 8) para manter o código claro, consistente e legível.

## Características Principais

 - Tipagem Forte: Garantimos que as variáveis em Nome da Linguagem de Programação sejam explicitamente tipadas, o que ajuda a evitar erros comuns.
 - Normas PEP 8: A obrigatoriedade das normas PEP 8 promove a consistência e a legibilidade do código em todo o ecossistema da linguagem.
 - A legibilidade do Python: A sintaxe da Nome da Linguagem de Programação é familiar para os desenvolvedores Python, tornando a transição suave.

## Exemplo: Two Sum Brute Force

```python
'''
Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.

You may assume that each input would have exactly one solution, and you may not use the same element twice.

You can return the answer in any order.

Input: nums = [2,7,11,15], target = 9
Output: [0,1]
Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].
'''

my_variable: int = 42

```
