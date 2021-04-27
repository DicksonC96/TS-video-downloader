for /l %%l in (0 1 9) do ren %%l.ts 000%%l.ts
for /l %%l in (10 1 99) do ren %%l.ts 00%%l.ts
for /l %%l in (100 1 999) do ren %%l.ts 0%%l.ts