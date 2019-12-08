#  Ordinals and Cardinals

Ordinals and cardinals are rather different, though they are related. They both contain the more well behaved finite objects and the stranger infinitely large "transfinite" objects.

## I just want programs

Sure.

Relevant files:

- `ordinal.py` - library for working with ordinals up to the Feferman–Schütte ordinal

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

Introduction to cardinals
---

TODO
