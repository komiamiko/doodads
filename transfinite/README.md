#  Ordinals and Cardinals

[Ordinals](https://en.wikipedia.org/wiki/Ordinal_number) and [cardinals](https://en.wikipedia.org/wiki/Cardinal_number) are rather different, though they are related. They both contain the more well behaved finite objects and the stranger infinitely large "transfinite" objects.

## I just want programs

Sure.

Relevant files:

- `ordinal.py` - library for working with ordinals up to the Feferman–Schütte ordinal (usually denoted **φ(1, 0, 0)** or **Γ₀**). Includes comparison, arithmetic, 2-argument Veblen function, fundamental sequences, and fast growing hierarchy expander.

## Introduction to ordinals

### What is an ordinal?

Ordinals are kind of like numbers but also kind of not like numbers, and they capture the concept of order types. Order types are a kind of reduced description of a set of things with a certain ordering on those things, which doesn't carry any information about the set or the ordering, only what the ordering "looks like". This is kind of like how I can have an object and only tell you its shape, and you can compare that shape to the shapes of other objects, without knowing what the object is made of.

#### What is an order type?

Well, what can an ordering "look like", exactly?

Let's take a a group of 4 people, waiting in a line. We might say there is a front of the line, second in line, third in line, and fourth in line. These form an ordering of 4 people.

We could also look at a group of 4 friends together, named Alex, Bee, Cam, and Dani. You could order them by their names alphabetically, this would result in *Alex < Bee < Cam < Dani*. You could also reverse the order, resulting in *Dani < Cam < Bee < Alex*.

You could take the 4 rocky planets and order them by their distance from the sun, or by their size. You could take 4 numbers and order them by their usual ordering. You could take any 4 things and order them in any way.

What is common to all these sets and orderings is that it ultimately "looks like" *0 < 1 < 2 < 3*, with those numbers substituted for whatever things you wanted. This "look-like", *0 < 1 < 2 < 3*, is an order type. We give it the name **4**, because there are 4 things in it.

In general, we could take a counting number **n**, and make that the name of the order type *0 < 1 < 2 < 3 < ⋯ < n-2 < n-1*. It will start counting at *0*, and count *n* different numbers. Said another way, it is all the numbers less than *n*, ordered in their usual way.

### Things you can do with order types

So far, we're still in the land of finite order types. They're called finite because you can count to them and they don't go on forever. If they did go on forever, they'd be infinite. There's plenty of cool things to see in the infinite lands, but we should first understand what happens in the finite lands before we go to the strange infinite lands.

#### The zero ordinal

Let's start with **0**. What's **0**? Well, it's nothing. There's nothing to order. All the things less than **0** is nothing. (shh, negative numbers don't exist for now) It's an empty order type. It is important though, and it plays a role in math. So we give it a name, and that is **0**.

#### Successor ordinals - how to count up in ordinals

So, how do we get from **n** to **n+1**? Well, we just add in a new thing, and make it considered to be after everything already in the order type. So for example, with those 4 friends earlier, you could add in another friend named Envy, and make Envy come after everyone else in the order type. So *Alex < Bee < Cam < Dani < Envy*, and that went from **4** to **5**. We can then go from **5** to **6** by adding in another friend, Fae, who again comes after everyone already in the group. So *Alex < Bee < Cam < Dani < Envy < Fae*, and that makes *6*.

Interestingly, or maybe not interestingly, going from **0** to **1** is... exactly as you'd expect it to be. For example, with the friends, you add Alex to an empty group, and the ordering is, well, Alex, which makes *1*. You can then add Bee to go from **1** to **2**, and so on. There's nothing unusual about the jump from **0** to **1**.

#### Ordinal addition

So let's look at what it means to add ordinals. **n + m** just means to take everything in **n** and everything in **m**, and put them together in a bigger group, and make everything in **m** come after everything in **n**. An easier way to think about it is gluing the 2 lists together. For example, let us take the group with *Alex < Bee*, and then glue on *Cam < Dani < Envy*. This represents **2 + 3**. The result is *Alex < Bee < Cam < Dani < Envy*, which we know is **5**. So **2 + 3 = 5**. Are you surprised?

#### Ordinals being equal

What about equality of ordinals? What does it mean for 2 order types to be equal? Well, it means that you can pair up items in one order type with items in the other order type in a way that the ordering looks exactly the same.

For example, *Alex < Bee < Cam < Dani* and *Mercury < Venus < Earth < Mars* both correspond to the ordinal **4**, so it makes sense that they should be equal. Then, let's show it by pairing them up:

```
Alex    < Bee   < Cam   < Dani
Mercury < Venus < Earth < Mars
```

Success! Those are equal.

What about *Alex < Bee < Cam < Dani* and *Triangle < Square < Pentagon*? Well, one is **4** and the other is **3**, so if we try to pair them up, we'll see that we can't do it. There's just no way to pair them up and keep the ordering, so these order types are not equal.

#### Ordinals being less than other ordinals

One more thing before we move on is the ordering of ordinals. What? Ordering of ordinals? Well, there is a way to define when an ordinal is less than or greater than another ordinal. We use a similar pairing thing to the equality, but instead of trying to pair them up exactly, we show that you pair up everything in one and then the other still has some things that aren't paired.

So, armed with this knowledge, let's see that *Alex < Bee < Cam < Dani* is greater than *Triangle < Square < Pentagon*. **4** is clearly bigger than **3**, so we're expecting this to work out.

```
Alex     < Bee    < Cam      < Dani
Triangle < Square < Pentagon   ▽▽▽▽
```

We paired up everything in the lower order type and then ran out of things, and the upper one still had *Dani* not matched with anything. So that's how we know *Alex < Bee < Cam < Dani* is greater than *Triangle < Square < Pentagon*. This says ***4** > **3***. Surprised?

You'll see what multiplication looks like later. For now though, we know enough to make a meaningful trip into the near reaches of the infinite lands.

### The first infinite ordinal, ω

What is the order type of all the counting numbers? Well, it goes *0 < 1 < 2 < 3 < ⋯*, and... it doesn't end. All of the finite order types so far had a first and last item, but this one only has a first. It has no last item. There is no largest counting number. You name a number, I can always add *1* and get a larger number. So now we have something new.

This order type is given the name of **ω**, the Greek letter omega. This is our first infinite ordinal.

#### Counting up from ω

What does **ω + 1** look like? Well, we can appeal to the rule that takes us from **n** to **n + 1**. Let's take all the counting numbers, and throw in a sun symbol: ☀. We'll say that ☀ is after all of the counting numbers. So the order type is *0 < 1 < 2 < 3 < ⋯ < ☀*, and this is named **ω + 1**.

Notice, since there is no highest counting number, that there is nothing directly before ☀. Everything else is less than ☀, yet there is nothing before it. This would be like being in an infinitely long line, without having someone who is directly in front of you. How strange!

Also, unlike **ω**, **ω + 1** does have a last item - it's ☀.

Then we can go to **ω + 2**. Let's throw in a moon: ☾. ☾ will be after everything in **ω + 1**. Then **ω + 2** looks like *0 < 1 < 2 < 3 < ⋯ < ☀ < ☾*.

#### A small note on writing out order types

Mathematicians don't use the sun and moon symbols for this. More commonly, they write the order types with all the ordinals less than that ordinal. It's like how before, we wrote **4** as *0 < 1 < 2 < 3* - this is everything up to *4*, but not including *4* itself. If we wanted to include the ordinal itself, we would run into problems with **ω**, because *ω* is a single thing larger than all the counting numbers, but we know **ω** is not allowed to have a last item. When we write **ω + 2**, we can write it as *0 < 1 < 2 < 3 < ⋯ < ω < ω + 1* and it all works out.

#### Where would ω + 1 actually come up?

We can build **ω + 1** using only the counting numbers, simply by shoving *0* to the back of the ordering. So we get *1 < 2 < 3 < 4 < ⋯ < 0*.

This sounds useless. Like, why would anyone want to define an ordering like this? Well, this one does have a use. *0* plays the role of an infinity, a number bigger than all the other numbers.

Also, in the standard 52-card deck, the Ace is actually the number *1*, but many card games treat it as the largest card, so if you're familiar with card games, shoving the first item to the back shouldn't be a new and unseen idea to you.

#### How does ω compare to ω + 1?

Something you might have thought of at this point is the ordering or equality. Why must ***ω** < **ω + 1*** be the case?

Well, try pairing them up!

To make it easier to talk about them, let's put some different names for the order types.

> ***ω** = A0 < A1 < A2 < A3 < ⋯*

> ***ω + 1** = B0 < B1 < B2 < B3 < ⋯ < C0*

Well, the obvious pairing works nicely, showing ***ω** < **ω + 1***:

```
A0 < A1 < A2 < A3 < ⋯   △△
B0 < B1 < B2 < B3 < ⋯ < C0
```

Anything else is doomed to fail. You won't be able to pair them up in a way that shows ***ω** = **ω + 1*** or ***ω** > **ω + 1***, because nothing can possibly pair up with *C0*. *C0* has the property that it is the last item of **ω + 1**. But there's no last item of **ω** for you to pair it up with.

#### 1 + ω is... ω?

Let's use the addition rule to combine **1** and **ω** to make **1 + ω**. What is **1 + ω**, exactly?

Well, let's write out the order types and see.

> ***1** = A0*

> ***ω** = B0 < B1 < B2 < B3 < ⋯*

> ***1 + ω** = A0 < B0 < B1 < B2 < B3 < ⋯*

If you thought that this looks exactly like **ω**, you're right. Just to be sure, we can pair them up.

```
B0 < B1 < B2 < B3 < B4 < ⋯
A0 < B0 < B1 < B2 < B3 < ⋯
```

There it is, every item of **ω** paired up with every item of **1 + ω**. So ***1 + ω** = **ω***. Also interestingly, **1 + ω** is not the same as **ω + 1**, and you saw how that happened.

This looks like it breaks some rule about addition, that when you flip the things you're adding you get the same thing. But all we did was use our own rule for addition. We didn't do anything wrong. Actually, for ordinal addition, it's not always true that you can flip the things you're adding and get the same result, and we just saw that happen.

### Reaching ω + ω

Let's go higher! What's **ω + ω**? We know how to add, we just glue together the order types.

> ***ω + ω** = A0 < A1 < A2 < A3 < ⋯ < B0 < B1 < B2 < B3 < ⋯*

So a neat thing about **ω + ω** is that it has no last item, but there's also some other item *B0* in there which has nothing directly before it. *B0* also comes after an infinite number of other things, and has an infinite number of other things coming after it.

We'd expect that ***ω** < **ω + ω***. Indeed, if you try to pair them up, there is nothing in **ω** that can take the role of *B0* in **ω + ω**.

#### Addition does not care about the order of gluing

Even though we did lose one nice thing about addition, we still have something else. Addition is based on gluing together order types. While it does matter which is on the left and which is on the right, it does not matter which order the gluing is done in, so for example, ***(ω + 1) + ω** = **ω + (1 + ω)***, which as you know, is equal to **ω + ω**.

This is somewhat like how if you are building a tower of blocks, the tower looks the same no matter what order you assemble the blocks in as long as you keep the blocks in the correct order, but if you change the order of the blocks then you end up with a different tower.

#### Up to ω + ω + ω

We can take **ω + ω** and add another **ω** to get **ω + ω + ω**.

> ***ω + ω + ω** = A0 < A1 < A2 < A3 < ⋯ < B0 < B1 < B2 < B3 < ⋯ < C0 < C1 < C2 < C3 < ⋯*

If you're still skeptical about the ordering being sensible, you might think, aha, surely we can pair up **ω + ω** and **ω + ω + ω** now! But no, that pairing will fail. You will first need to find something to take the role of *B0*, which you can do, because **ω + ω** already contains it. But then you need something to take the role of *C0*, which has infinite items after it, and infinite items before it but after *B0*. And there's nothing like that in **ω + ω**. So as expected, we are left with ***ω + ω** < **ω + ω + ω***.

#### Defining ordinal multiplication

Adding something to itself makes you want to write it as a multiplication. Like, surely we can write ***ω + ω** = **ω × 2***, and ***ω + ω + ω** = **ω × 3***, right?

Well, first, we should probably come up with a rule for what it means to multiply ordinals.

As you might guess, we define **n × m** to be the ordinal **n**, repeated *m* times.

We're very particular about which is the left and right side because, as you might guess, just like addition, it does matter which is the left and right side.

#### What is 2 × ω?

**ω × 2** is not very interesting, because by our rule, that means **ω** repeated *2* times, so it could not possibly be anything other than **ω + ω**.

What about **2 × ω**? Well, it's **2** repeated... *ω* times. It's a little scary to imagine what repeating something an infinite number of times means, so let's just write it out.

> ***2 × ω** = A0 < A1 < B0 < B1 < C0 < C1 < D0 < D1 < E0 < E1 < ⋯*

We're right back at **ω**. So ***2 × ω** = **ω***.

### Higher arithmetic with ordinals

Fair warning, beyond here, we start going into some of the more complicated math. It becomes unavoidable to invoke some big scary demons. Don't feel bad if you have trouble following.

By the way, counting numbers are more typically called "natural numbers" by mathematicians. Also, nobody agrees if it should start at *0* or *1*. We start at *0* in ordinals because that's most sensible and useful.

You should trust that ordinal arithmetic is a thing by now. So let's go higher!

### Getting to ω × ω

What happens when we take **ω × ω**? It will be **ω** repeated *ω* times.

This order type actually does correspond to something meaningful. If we take all the pairs of counting numbers, and order them first by the first number, then by the second, we get an order type exactly matching **ω × ω**:

```
  (0, 0) < (0, 1) < (0, 2) < (0, 3) < ⋯
< (1, 0) < (1, 1) < (1, 2) < (1, 3) < ⋯
< (2, 0) < (2, 1) < (2, 2) < (2, 3) < ⋯
< (3, 0) < (3, 1) < (3, 2) < (3, 3) < ⋯
  ⋮        ⋮        ⋮        ⋮        ⋱
```

If this grid is a little scary, just remember, it's *ω* copies of **ω**.

### Powers of ordinals

Now that we built **ω × ω**, it's pretty natural to ask about powers. Could we write it as **ω²**?

Yes, we could. We can go up to **ω²**, **ω³**, and then up to **ωʷ**.

This is the one time you'll see a "matchstick diagram". They're pretty but usually not very useful. Here though they provide a nice visual representation of **ωʷ**.

![Matchstick diagram for ωʷ, laid out as a spiral. Starts at 0, spirals inward, each turn corresponding to ω, ω², ω³, ω⁴, and so on, with ωʷ placed in the middle to say that's what the sequence tends toward at the limit. ](https://upload.wikimedia.org/wikipedia/commons/thumb/e/e6/Omega-exp-omega-labeled.svg/600px-Omega-exp-omega-labeled.svg.png)

**ωʷ** is still comprehensible. It's the order type of all the finite lists of counting numbers, ordered first by their length, then by the first number, then the second, and so on. We can write it out, with some difficulty.

```
  ()
< (0) < (1) < (2) < (3) < ⋯
< (0, 0) < (0, 1) < (0, 2) < (0, 3) < ⋯
< (1, 0) < (1, 1) < (1, 2) < (1, 3) < ⋯
< (2, 0) < (2, 1) < (2, 2) < (2, 3) < ⋯
< (3, 0) < (3, 1) < (3, 2) < (3, 3) < ⋯
  ⋮        ⋮        ⋮        ⋮        ⋱
< (0, 0, 0) < (0, 0, 1) < (0, 0, 2) < (0, 0, 3) < ⋯
< (0, 1, 0) < (0, 1, 1) < (0, 1, 2) < (0, 1, 3) < ⋯
< (0, 2, 0) < (0, 2, 1) < (0, 2, 2) < (0, 2, 3) < ⋯
  ⋮           ⋮           ⋮           ⋮
< (1, 0, 0) < (1, 0, 1) < (1, 0, 2) < (1, 0, 3) < ⋯
< (1, 1, 0) < (1, 1, 1) < (1, 1, 2) < (1, 1, 3) < ⋯
< (1, 2, 0) < (1, 2, 1) < (1, 2, 2) < (1, 2, 3) < ⋯
  ⋮           ⋮           ⋮           ⋮
< (2, 0, 0) < (2, 0, 1) < (2, 0, 2) < (2, 0, 3) < ⋯
< (2, 1, 0) < (2, 1, 1) < (2, 1, 2) < (2, 1, 3) < ⋯
< (2, 2, 0) < (2, 2, 1) < (2, 2, 2) < (2, 2, 3) < ⋯
  ⋮           ⋮           ⋮           ⋮
< (0, 0, 0, 0) < (0, 0, 0, 1) < (0, 0, 0, 2) < (0, 0, 0, 3) < ⋯
  ⋮              ⋮              ⋮              ⋮              
< (0, 0, 0, 0, 0) < (0, 0, 0, 0, 1) < (0, 0, 0, 0, 2) < (0, 0, 0, 0, 3) < ⋯
  ⋮                 ⋮                 ⋮                 ⋮                 
< (0, 0, 0, 0, 0, 0) < (0, 0, 0, 0, 0, 1) < (0, 0, 0, 0, 0, 2) < (0, 0, 0, 0, 0, 3) < ⋯
  ⋮                    ⋮                    ⋮                    ⋮   
```

#### Fixed points and ε₀

By taking the limit of **1 + 1 + 1 + ⋯**, we got **ω**, which is the first "fixed point" of *(β ↦ 1 + β)*, that is, the first *β* that can satisfy *β = 1 + β*. Indeed, *ω = 1 + ω*.

By taking the limit of **ω + ω + ω + ⋯**, we got **ω²**, which is the first fixed point of *(β ↦ ω + β)*.

By taking the limit of **ω × ω × ω × ⋯**, we got **ωʷ**, which is the first fixed point of *(β ↦ ω × β)*.

By taking the limit of **ω ^ ω ^ ω ^ ⋯**, we get a new special ordinal, called **ε₀**, which is the first fixed point of *(β ↦ ωᵝ)*.

#### An ordering with order type ε₀

Going beyond lists of numbers, we can actually find a collection of something and an ordering for it with order type **ε₀**. It'll be a lot easier to describe this in terms of how those things map to ordinals below **ε₀**, so we'll do it that way.

The collection of things is the set of rooted unlabeled trees. Let *F(s)* be the ordinal corresponding to a subtree *s*. *F(s) = ω^F(c₀) + ω^F(c₁) + ω^F(c₂) + ⋯*, where *c* are the children of *s*.

We can draw out some trees and see what ordinals they correspond to. Here we'll put the root at the top and have the tree extend down.

```
0

o

1

o
|
o

2

o
├-┐
o o

3

o
├-┬-┐
o o o

n

o
├-┬-┬-⋯-┐
o o o   o

ω

o
|
o
|
o

ω + 1

o
├-┐
o o
|
o

ω × 2

o
├-┐
o o
| |
o o

ω ^ 2

o
|
o
├-┐
o o

ω ^ 2 + ω

o
├---┐
o   o
├-┐ |
o o o

ω ^ ω

o
|
o
|
o
|
o

ω ^ ω ^ ω

o
|
o
|
o
|
o
|
o
```

You could show that this is indeed a bijection between rooted unlabeled trees and ordinals under **ε₀**, and since we know how to order ordinals up to **ε₀**, we know how to order these trees.

### More stuff with ordinals

The *0* subscript of **ε₀** suggests you can go further, and that perhaps there is a **ε₁**, and more, and even a fixed point of *(β ↦ εᵦ)*. Yes, there is, and you can go much further. Go explore the Veblen functions on your own if you like. Beyond even those are strange beasts like the Bachmann-Howard ordinal, defined using an Ordinal Collapsing Function and the first uncountable ordinal.

You've been presented here with a way of looking at ordinals using the order types, though there's a mostly equivalent formulation, a bit higher level and more useful for defining arithmetic, which is the Von Neumann definition of ordinals. Instead of using order types, it's entirely set theoretic.

We've also skipped out on the proper definitions of zero, successor, and limit ordinals, as well as fundamental sequences.

Larger ordinals are also the "proof-theoretic ordinals" of some commonly used mathematical theories. Anything less than that ordinal is fine to the theory, but that ordinal and above causes problems for that theory.

Ordinals also find uses in googology, coupled with a Fast Growing Hierarchy to define extremely large numbers.

### Bonus - cardinalities of ordinals

You might want to read the section on cardinals first, and then get back here.

If you ignore the ordering within an ordinal, you may just look at how many things it orders. This would be its cardinality.

Because there exists a bijection between 2 sets with the same cardinality, this means that every countably infinite ordinal (so from **ω** up to **ω₁**) can have the ordinals less than it mapped one-to-one with the counting numbers. And when you do this map, you can carry the ordering over. By doing this, you can get unusual orderings on the counting numbers corresponding to whatever countably infinite ordinal you want.

#### Even and odd

We briefly mentioned **ω + 1** as emulating the order type of the counting numbers with a special number designated as infinity. We have another slightly interesting ordering to show.

Suppose we put all the even numbers before all the odd numbers. The ordering looks like:

***ω × 2** = 0 < 2 < 4 < 6 < ⋯ < 1 < 3 < 5 < 7 < ⋯*

Most of the time though, when you build an ordering on the counting numbers made to reflect a certain ordinal, it's just weird and not very interesting.

#### An alternate ordering of unlabelled rooted trees

The unlabelled rooted trees have the same cardinality as the natural numbers, so unsurprisingly, there's an ordering for those trees matching any countably infinite order type you can name. We showed you a way to order them like **ε₀** before. And now, we'll show you one that emulates a much larger ordinal. Though we haven't checked it ourselves, this ordering is claimed to have order type the small Veblen ordinal (SVO).

Given 2 trees *A* and *B*, how should we order them? Well, first, if *A ≤ C* for any *C* which is an immediate child of *B*, then *A < B*. Similarly, if *B ≤ C* for any *C* which is an immediate child of *A*, then *B < A*. We have more tiebreaking to do after this. If *A* has less children than *B*, then *A < B*. If *B* has less children than *A*, then *B < A*. Last tiebreaking step, now knowing they have the same number of children. Sort *A*'s children as *a₀ ≤ a₁ ≤ ⋯ ≤ aᵤ* and *B*'s children as *b₀ ≤ b₁ ≤ ⋯ ≤ bᵤ*. If they're identical, then *A = B*, as you might guess. Otherwise, let *aᵨ, bᵨ* be the first pair that differs. Then order *A* and *B* by the ordering of *aᵨ* and *bᵨ*.

#### What ordinals are they?

What ordinals these trees correspond to is not very obvious. We'll write the trees in full again, root at the top.

The zero ordinal is the easiest to figure out. After all, nothing can go lower than a node with no children.

```
0

o
```

We'll be reaching into the higher ordinals if we allow many children, so let's count up with *1* child at most for now.

```
1

o
|
o

2

o
|
o
|
o
```

You might take a guess now that the successor of whatever ordinal is represented by tree *β* is just a node with *β* as its only child, and indeed, this seems to be the case. If you try writing out all the trees with some number of nodes or less, and then sort them, you'll find this kind of tree always follows another smaller tree - so it has to be the successor.

```
β + 1

o
|
β
```

#### From ω to ω²

The smallest tree with a node with 2 children would have to be **ω**.

```
ω

o
├-┐
o o
```

From there, the pattern continues counting up **ω + n**. The smallest step other than succession would have to be **ω × 2**, and after playing around with it a bit, there ends up being only one possible way to build it.

```
ω × 2

o
├-┐
o o
|
o
```

The pattern continues with **ω × 3**.

```
ω × 3

o
├-┐
o o
|
o
|
o
```

More generally...

```
ω × (1 + β)

o
├-┐
B o
```

This rule even works for *β = ω*, and gives the correct tree.

```
ω²

o
├-┐
o o
├-┐
o o
```

... though it breaks for some larger *β*.

#### From ω² to ω³

Taking steps in the middle adds copies of **ω**...

```
ω² + ω

o
├-┐
o o
|
o
├-┐
o o

ω² + ω × 2

o
├-┐
o o
|
o
|
o
├-┐
o o
```

Taking steps at the end adds copies of **ω²**...

```
ω² × 2

o
├-┐
o o
├-┐
o o
|
o

ω² × 3

o
├-┐
o o
├-┐
o o
|
o
|
o
```

And then up to **ω³** by adding another layer with 2 children.

```
ω³

o
├-┐
o o
├-┐
o o
├-┐
o o
```

#### From ω³ to ωʷ

**ω³** extends the pattern of lengthening chains to add intermediate entries:

```
ω³ + 1

o
|
o
├-┐
o o
├-┐
o o
├-┐
o o

ω³ + ω

o
├-┐
o o
|
o
├-┐
o o
├-┐
o o

ω³ + ω²

o
├-┐
o o
├-┐
o o
|
o
├-┐
o o

ω³ × 2

o
├-┐
o o
├-┐
o o
├-┐
o o
|
o
```

You can keep adding more layers and the pattern continues.

The first ordinal to break this pattern must be **ωʷ**, and after that it gets more confusing so we won't show beyond **ωʷ**.

```
ωʷ

o
├-┐
o o
| |
o o
```

## Introduction to cardinals

### What are cardinals?

Cardinals are somewhat like numbers, but also a little different. They capture the concept of the sizes of sets, as in, the number of elements in a set. Holding even less information than ordinals, cardinals don't tell you how things are ordered, only how many things there are. Strange things happen in the lands of infinite cardinals, different from what happens in the lands of infinite ordinals.

#### Counting how many things there are

We still should start at the basics. Math speak for how many things are in a set is the "cardinality" of that set, and that count is a cardinal. So let's take some cardinalities (cardinals) of some sets we know, and start giving them names.

How many things are there in nothing? Well, we would say **0**. So **0** is the cardinality of the empty set, *{}*. We would write this as ***0** = | {} |*. The vertical bar brackets are how you write "take the cardinality of this".

Now let's add a thing to our set, say, Alex. So we have *{Alex}*. How many things are there in this set? Well, we'd say **1**. So the name of the cardinality of this set is **1**. We write ***1** = | {Alex} |*. It also happens to be the cardinality of every other set imaginable with *1* thing in it. That's what the cardinality is, after all, it counts how many things are in there.

We add another thing, maybe a few more. Maybe we now have *{Alex, Bee, Cam, Dani, Envy, Fae}*. We count, and there's *6* things in there, so the cardinality is **6**. ***6** = | {Alex, Bee, Cam, Dani, Envy, Fae} |*.

Every counting number is a cardinal, the cardinal for every set with that number of things in it. Make sense?

### Comparison of cardinals

Let's say we have **μ** (the Greek letter mu) which is the cardinality of a set *M*, and **κ** (the greek letter kappa) which is the cardinality of a set *K*.

What it means for **μ** and **κ** to be equal is that it is possible to pair up the items of *M* and the items of *K* one-to-one. In mathematical fancy talk, a one-to-one mapping is called a "bijection" - prefix "bi-" for 2 and "-jection" like injection.

We can pair up all the items of *{Alex, Bee, Cam, Dani}* with all the items of *{1, 2, 3, 8}* and also with all of the items of *{▱, ▲, ◉, ▵}*, and that would show that their cardinalities are all equal, and we never have to mention the number **4**!

```
Alex ↔ 1 ↔ ▱
Bee  ↔ 2 ↔ ▲
Cam  ↔ 3 ↔ ◉
Dani ↔ 8 ↔ ▵
```

How we pair them up isn't important for showing that the cardinalities are equal. It only matters whether we can pair them up at all.

#### Bigger and smaller cardinals

If **μ** and **κ** are not equal, then one of them has to be the bigger cardinal. So, let's say **μ** is less than **κ**. What would this mean?

**μ** being less than **κ** means that when you match up all the items of *M* with items of *K*, you'll end up using up all the items of *M* and then still have items of *K* that haven't been matched up. Or, said another way, if you match up every item in *K* with an item in *M*, you will certainly have some 2 items of *K* matched up with the same item of *M*, because there just aren't enough things in *M* to match them up without repeats.

To show this both ways, we'll compare *{Envy, Fae}* and *{☀, ☁, ☂}*.

In the first way, we match up items of *{Envy, Fae}* with items of *{☀, ☁, ☂}* and then we'll be doomed to run out of items in *{Envy, Fae}* before everything in *{☀, ☁, ☂}* gets matched up.

```
Envy ↔ ☀
Fae  ↔ ☁
???  ↔ ☂
```

In the second way, we match up every item in *{☀, ☁, ☂}* with an item of *{Envy, Fae}* and then be forced to repeat something in *{Envy, Fae}*.

```
☀ → Envy
☁ → Fae
☂ → ???
```

Well, we tried our best, but no matter what you choose to match *☂* with, you're forced to repeat *Envy* or *Fae*.

### Addition of cardinals

For cardinal arithmetic, it makes sense to start with addition.

We have ***μ** = | M |* and ***κ** = | K |*, and let's say we want to find out what the cardinal **μ + κ** is.

Well, first, we need *M* and *K* to not have overlaps, meaning no item in common. You can get rid of overlaps by replacing items. We know by the rule about one-to-one pairing that this replacing won't change **μ** or **κ**.

Then, we build a new set which contains everything from both *M* and *K*. The way to write this is *M ∪ K*, with that *∪* ("union" symbol) meaning "every item contained in at least one of those sets".

Now we just have to take the cardinality of (count how many things are in) *M ∪ K*, and that cardinality is **μ + κ**.

#### An example of addition

Let's say we want to add ***μ** = | {Alex, Bee, Cam} |* and ***κ** = | {Cam, Dani} |*. Here we can count ***μ** = **3*** and ***κ** = **2***, so we're expecting to get ***μ + κ** = **5***.

First, let's get rid of the overlaps. In the second set, we'll replace *Cam* with *Envy*, so we have ***κ** = | {Dani, Envy} |*.

Now we can merge the sets and get *{Alex, Bee, Cam, Dani, Envy}*. If we count how many things there are, we will get ***3** + **2** = **5***.

### Multiplication of cardinals

Same situation again, but this time we want to figure out what the cardinal **μ × κ** is.

We don't need to get rid of overlaps this time. It's fine to leave both sets as they are.

**μ × κ** counts how many different ways we can make a pair by taking the first item from *M* and taking the second item from *K*. It's important that the order of the pair matters, meaning *(Alex, Bee)* as a pair is not the same as *(Bee, Alex)* as a pair.

By the way, this set of all the pairs is written as *M × K*. That *×* is given the fancy name "Cartesian product", but it really just means "all the pairs".

#### An example of multiplication

This time we want to multiply ***μ** = | {Alex, Bee, Cam} |* and ***κ** = | {Cam, Dani} |*. We could count ***μ** = **3*** and ***κ** = **2***, so we're expecting to get ***μ × κ** = **6***.

What are all the possible pairs? Well, we could make a chart to find out.

```
          | (?,    Cam) | (?,    Dani)
----------┼-------------┴-------------
(Alex, ?) | (Alex, Cam)   (Alex, Dani)
(Bee,  ?) | (Bee,  Cam)   (Bee,  Dani)
(Cam,  ?) | (Cam,  Cam)   (Cam,  Dani)
```

Cam is paired with Cam. So what?

We count **6** different pairs. So ***3** × **2** = **6***.

### Powers of cardinals

The last of the common operations, powers. What would **μᴷ** be?

It is the number of ways to choose from **μ** different things, **κ** times. Or, if we want to talk about them using the sets, it is the number of ways to assign an item in *M* to each item in *K*.

#### An example of a power

Let's say we want to find **μᴷ**, with ***μ** = | {Alex, Bee, Cam} |* and ***κ** = | {Cam, Dani} |*. How many ways can we do this kind of matching?

Well, for starters, the *Cam* in *K* can be matched with any of *{Alex, Bee, Cam}*...

```
     ┌→ Alex
Cam -┼→ Bee
     └→ Cam
```

And from there, the *Dani* in *K* can be matched with any of *{Alex, Bee, Cam}*...

```
                    ┌→ Alex
     ┌→ Alex, Dani -┼→ Bee
     |              └→ Cam
     |              ┌→ Alex
Cam -┼→ Bee,  Dani -┼→ Bee
     |              └→ Cam
     |              ┌→ Alex
     └→ Cam,  Dani -┼→ Bee
                    └→ Cam
```

In the end, we count **9** different ways to do this matching. So ***3²** = **9***.

### Counting to infinity

So far, we only worked with finite sets, and everything worked like we'd expected to.

Let's now introduce our first infinitely large set, which everyone can agree is the smallest one. It's the counting numbers, or the "natural numbers" as mathematicians call it. We give it the name *ℕ*, which is a capital Latin letter *N* written in a "blackboard bold" font. If you need to write it yourself, just put 2 lines instead of 1 in the N.

*ℕ = {0, 1, 2, 3, 4, ⋯}*

Mathematicians diagree over whether *ℕ* should include *0*. A lot of the times, it's useful to include *0*, because *0* is a useful number, but other mathematicians say nobody actually starts counting at *0* so it should start at *1* instead, or that *0* sometimes causes problems. For the sake of counting how many there are, it really doesn't matter.

To show just how much it doesn't matter for cardinality, we'll show that *ℕ* with *0* and *ℕ* without *0* have the same cardinality.

```
0 ↔ 1
1 ↔ 2
2 ↔ 3
3 ↔ 4
⋮   ⋮
```

With an infinite number of things, it's not so easy to say we would ever "run out" of things, but we can see that this maps them one-to-one - every number on the left finds something on the right to pair with, and every number on the right finds something on the left to pair with. This one-to-one mapping existing tells us the cardinality of both is the same.

#### A name for the cardinality of the counting numbers - ‎א‎₀

The common name for the size of the counting numbers, which is the first infinite cardinal, is **‎א‎₀**, using the Hebrew letter Aleph/Alef and a subscript *0* to say it's the first. Really, *0*, not *1*. Kind of like the ordinal counting with *0* first.

***‎א‎₀** = | ℕ |*

### Subsets

A topic we skipped earlier is "subsets". Made of the prefix "sub-" for "part of" and "set" which are the sets we know. A subset of a set is part of that set. More specifically, a subset is a set where every item in it is also in the original set.

For example, *{Alex, Bee}*, *{}*, and *{Alex, Bee, Cam}* are all subsets of *{Alex, Bee, Cam}*, since every item in the subset is also in the other set. However, *{Cam, Dani}* is not a subset of that set, because there is *Dani* which is not in *{Alex, Bee, Cam}*.

What can we say about the cardinalities of subsets? Well, let's say we have ***μ** = | M |* and ***κ** = | K |* again, but now *M* is also a subset of *K*. Then ***μ** ≤ **κ***. The subset can't be larger, surely, or else it would have to contain something that the other set doesn't have. It may be equally large. Or it may be smaller. So ***μ** ≤ **κ*** is the most we can say. It's already quite useful though.

### There are just as many even numbers

We can separate *ℕ* into the even numbers and the odd numbers. Surely there are less even numbers than all the counting numbers, right? That would be a good guess. After all, there are the odd numbers which are in the counting numbers but not in the even numbers.

Well, we can pair up all the even numbers with all of the counting numbers, and because we can do this, they must have the same cardinality.

```
0 ↔ 0
1 ↔ 2
2 ↔ 4
3 ↔ 6
4 ↔ 8
⋮   ⋮
```

But wai! That seems strange. There are also as many even numbers as odd numbers, and together they make up the counting numbers, so then...

***‎א‎₀** + **‎א‎₀** = **‎א‎₀** × **2** = **‎א‎₀***

It sounds wrong, but by the rules we set out, it couldn't be anything else. Accept that infinite cardinals behave strangely.

### A diagonal jump

More strange things happen in the lands of infinite cardinals. One of the things we might ask is, how many pairs of counting numbers are there? Maybe that would be larger than **‎א‎₀**?

Well, let's make another chart to list out all the pairs:

```
       | (?, 0) | (?, 1) | (?, 2) | (?, 3) | ⋯
-------┼--------┴--------┴--------┴--------┴---
(0, ?) | (0, 0)   (0, 1)   (0, 2)   (0, 3)   ⋯
(1, ?) | (1, 0)   (1, 1)   (1, 2)   (1, 3)   ⋯
(2, ?) | (2, 0)   (2, 1)   (2, 2)   (2, 3)   ⋯
(3, ?) | (3, 0)   (3, 1)   (3, 2)   (3, 3)   ⋯
   ⋮   |    ⋮        ⋮        ⋮        ⋮
```

As it turns out, we can walk along the diagonals and match up each pair with a counting number.

```
       | (?, 0) | (?, 1) | (?, 2) | (?, 3) | ⋯
-------┼--------┴--------┴--------┴--------┴---
(0, ?) |    0        1        3        6     ⋯
(1, ?) |    2        4        7       11     ⋯
(2, ?) |    5        8       12       17     ⋯
(3, ?) |    9       13       18       24     ⋯
   ⋮   |    ⋮        ⋮        ⋮        ⋮
```

That's how we know ***‎א‎₀** × **‎א‎₀** = **‎א‎₀²** = **‎א‎₀***.

Now that we know ***‎א‎₀²** = **‎א‎₀***, we can go further and say ***‎א‎₀ⁿ** = **‎א‎₀*** for every finite **n** which is at least **1**.

### Infinite cardinals still play nicely

While some of the things infinite cardinals do looks strange, there are still some nice things they do. The ordering is sane, in the sense that all cardinals can be compared and you won't end up with nonsensical loops like *μ < κ < ν < μ*. Addition and multiplication don't care which is left and which is right. Addition, multiplication, and powers are all increasing (or at the very least, not decreasing) where you expect them to be increasing.

### Power sets

There's another thing called a "power set". The power set of a set is the set of all its subsets. That's a mouthful, so let's see an example.

What are all the subsets of *{Alex, Bee, Cam}*? Well, they are *{}, {Alex}, {Bee}, {Cam}, {Alex, Bee}, {Alex, Cam}, {Bee, Cam}, {Alex, Bee, Cam}*. If we put that into a new set, we get *{{}, {Alex}, {Bee}, {Cam}, {Alex, Bee}, {Alex, Cam}, {Bee, Cam}, {Alex, Bee, Cam}}*

The power set is written with the capital Latin letter P (in cursive writing if you can) and brackets around the set you're taking the power set of. So here we'd write *P({Alex, Bee, Cam}) = {{}, {Alex}, {Bee}, {Cam}, {Alex, Bee}, {Alex, Cam}, {Bee, Cam}, {Alex, Bee, Cam}}*.

#### Cantor's theorem

Georg Cantor found something neat about power sets.

For a set *M*, we can match up every item in *M* with a set containing just that item, and that set is a subset of *M*, so *P(M)* must be at least as large as *M*. But is it larger?

Let's try to match up items in *M* with items of *P(M)*, and see what might go wrong. Let's say that, for every item in *M*, if we call it *X*, then we map it to *☆X*, which is one of those subsets of *P(M)*. Now we can build a new set, say, *Y*, which is the set containing every *X* that was not contained in *☆X*. No item *X* can possibly map to *Y*, because if it did, then *Y = ☆X*, and by the defininition of *Y*, *X* is in *Y* if and only if *X* is not in *Y = ☆X*, which can't make sense. Thus *Y* is an item of *P(M)* which no item in *M* maps to. We can always find such a *Y*, so this is always the case.

In the end, we must conclude *| P(M) | > | M |*, and this will hold for any set *M*, finite or not.

#### The size of the power set

So, how many items are in *P(M)*?

Well, each subset could also be seen as the result of asking "do I include this item?" for every item in *M*. That question can only be answered *yes* or *no*. This looks a lot like what we said exponentiation was.

And so we have *| P(M) | = 2 ^ | M |*.

We also know this is bigger than the size of the original set, so ***2ᵘ** > **μ*** for every cardinal **μ**.

### Counting up in the ‎ב‎ (beth) numbers

Another name for **‎א‎₀** is **‎ב‎₀**, using the Hebrew letter Beth/Bet. The ‎א‎ and ‎ב‎ numbers differ after the first, but the ‎ב‎ numbers are easier to understand, so we'll look at the ‎ב‎ numbers first.

‎ב‎ numbers use ordinals as subscripts. Don't worry about limit ordinals for now. Let's just see how to get from a ‎ב‎ number to the next.

***‎ב‎ᵦ₊₁** = **2** ^ **‎ב‎ᵦ***

It will certainly be larger than the last, because that's how power sets work.

#### What the ‎א‎ (aleph) numbers are

So, what exactly is different about the ‎א‎ numbers? Well, they don't follow such a straightforward sequence. Or maybe they do.

**‎א‎₀** is the first infinite cardinal. **‎א‎₁** is the second infinite cardinal. And so on.

You might think, well, aren't they the same as the ‎ב‎ numbers?

The thing is, how would you know that there aren't any infinite cardinals between **‎ב‎₀** and **‎ב‎₁**? There might be another, and it could be **‎א‎₁**. Or **‎א‎₁** could just be **‎ב‎₁**.

It's not known how many infinite cardinals are between **‎ב‎₀** and **‎ב‎₁**, or if there are any at all. At the very least, nobody has actually found a set with infinite cardinality between **‎ב‎₀** and **‎ב‎₁**. Our usual modern theories can't prove or disprove the existence of such a set. It's just a math mystery.

### The size of the integers

We're going a bit more mathy. Good on you if you followed up to here, but it's going to get harder from here.

The "integers", being the whole numbers - negative, zero, and positive all included - are commonly written as *ℤ*, a blackboard bold uppercase Latin letter Z.

It's not too hard to see that there's as many integers as counting numbers, so *| ℤ | = **‎א‎₀***.

```
⋯  5  3  1
            0  2  4  6 ⋯
⋯ -3 -2 -1  0 +1 +2 +3 ⋯
```

#### The size of the rationals

The "rational" numbers are all the fractions, including the fractions that are actually just integers. They're usually written as *ℚ*, a blackboard bold Q.

Every integer is also a rational number, so there must be at least as many rational numbers as there are integers. Every rational number can be written as *ᵘ/v* for some integers *u, v*, so there are at most as many rational numbers as there are pairs of integers.

Turns out, both of these sizes are **‎א‎₀**.

So we get ***‎א‎₀** ≤ |ℚ| ≤ **‎א‎₀***

#### The cardinality of the continuum

So that's a fancy famous phrase in mathematics. But really we're asking about the size of the real numbers. The real numbers are the rational numbers and everything inbetween - the roots, pi, every conceivable weird decimal number, and more. They're what you get when you fill in the gaps. It's usually written as *ℝ*, a blackboard bold R.

If we write out the decimal expansion (which may be infinitely long) of every real number, we end up writing up to **‎א‎₀** digits for each, and each of those digits can be *1* of **10** different things. If you're not convinced yet that there are up to **‎א‎₀** decimal digits, note that every digit can be assigned an integer indicating its position - you may say say the ones' digit is *0*, the tens digit is *1*, the hundreds is *2*, and so on, and for the fractional part, the 1/10 digit is *-1*, the 1/100 digit is *-2*, and so on.

The number of possible decimal expansions is ***10** ^ **‎א‎₀***, and this will hit every real number. There will also be many decimal expansions describing an infinitely large number, which isn't a real number. In any case this tells us there can't be more than ***10** ^ **‎א‎₀*** real numbers.

With a bit of trickery, we can say ***10** ^ **‎א‎₀** ≤ **16** ^ **‎א‎₀** = **2** ^ (**‎א‎₀** × **4**) = **2** ^ **‎א‎₀***. So ***2** ^ **‎א‎₀*** is our new upper limit on *| ℝ |*.

If we had limited ourselves to only using the digits *{3, 7}* (there are **2** of them) and forced the ones digit and larger to be all *0*, then we will end up building some subset of the reals. This subset has size ***2** ^ **‎א‎₀***, which sets a lower limit on *| ℝ |*.

Putting this together, we have ***2** ^ **‎א‎₀** ≤ | ℝ | ≤ **2** ^ **‎א‎₀***. So *| ℝ | = **2** ^ **‎א‎₀** = **‎ב‎₁***.

### Bonus - the value of ‎א‎₀ ^ ‎א‎₀

It should be pretty straightforward by now to convince yourself that ***n** ^ **‎א‎₀** = **‎ב‎₁*** for all finite **n** which is at least **2**. But what about ***‎א‎₀** ^ **‎א‎₀***?

Well, first, we know that the power operation is increasing (not decreasing), so ***2** ^ **‎א‎₀** ≤ **‎א‎₀** ^ **‎א‎₀***.

Now, we need a different way of thinking about what these represent.

You know how your computer stores data in binary form? Well, imagine a binary file with **‎א‎₀** bits. It wouldn't fit on any computer, but we can imagine it. The number of possible binary files with **‎א‎₀** bits is ***2** ^ **‎א‎₀***.

Now, let's imagine an infinitely long (with length **‎א‎₀**, specifically) sequence of counting numbers. The number of possible sequences like this is ***‎א‎₀** ^ **‎א‎₀***. Now, let's suppose there's some encoding, which turns counting numbers into strings of bits in a way that it could be decoded later with no confusion as to what number those bits represented. This encoding doesn't need to be efficient in any way, it can be any stupid encoding, as long as it can't cause *2* different sequences to get encoded to the same binary file.

As an example of a stupid encoding that works, we'll encode every counting number **n** as that many *1* bits followed by a *0* bit. This is "unary" encoding.

The number sequences, then encoded, hit some subset of the binary files of length **‎א‎₀**. So ***‎א‎₀** ^ **‎א‎₀** ≤ **2** ^ **‎א‎₀***.

Putting this all together again, we end up with ***‎א‎₀** ^ **‎א‎₀** = **2** ^ **‎א‎₀** = **‎ב‎₁***.
